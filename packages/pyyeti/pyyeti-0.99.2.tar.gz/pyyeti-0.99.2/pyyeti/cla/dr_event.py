# -*- coding: utf-8 -*-
"""
DR_Event: Setup data recovery for a specific event or set of modes
"""
import copy
from types import SimpleNamespace
import warnings
from collections import OrderedDict
import numpy as np
import scipy.linalg as la
from pyyeti.ytools import reorder_dict
from pyyeti.nastran import n2p
from .dr_results import DR_Results
from ._utilities import _merge_uf_reds


# FIXME: We need the str/repr formatting used in Numpy < 1.14.
try:
    np.set_printoptions(legacy="1.13")
except TypeError:
    pass


class DR_Event:
    """
    Setup data recovery for a specific event or set of modes.

    Attributes
    ----------
    Info : :class:`collections.OrderedDict`
        Contains data recovery information for each category. The
        category names are the keys. This is a copy of information in
        one or more `DR_Def` instances created during data recovery
        setup; eg, in a "prepare_4_cla.py" script. See :class:`DR_Def`
        and the example below. The copy is made during the call to
        :func:`DR_Event.add` and new values for the `uf_reds` option
        can be set during that call.
    UF_reds : list
        List of all unique 4-element uncertainty factor tuples. See
        :func:`DR_Def.add` for more information.
    Vars : dict
        Contains the data recovery matrices and possibly other data
        needed for data recovery. This is derived from the
        ``DR_Def['_vars']`` dict and the current system modes. See the
        notes section below for an example showing what is in this
        dict.

    Notes
    -----
    Here are some views of example data via :func:`pyyeti.pp.PP`. This
    would be after, for example::

        DR = cla.DR_Event()
        DR.add(nas, drdefs_for_se100)   # PAF data recovery
        DR.add(nas, drdefs_for_se500)   # SC data recovery
        DR.add(nas, drdefs_for_se0)     # recover "Node4"

    PP(DR, 2):

    .. code-block:: none

        <class 'pyyeti.cla.DR_Event'>[n=3]
            .Info   : <class 'dict'>[n=6]
                'PAF_ifatm': <class 'types.SimpleNamespace'>[n=20]
                'PAF_ifltm': <class 'types.SimpleNamespace'>[n=20]
                'SC_atm'   : <class 'types.SimpleNamespace'>[n=20]
                'SC_dtm'   : <class 'types.SimpleNamespace'>[n=20]
                'SC_ltm'   : <class 'types.SimpleNamespace'>[n=20]
                'Node4'    : <class 'types.SimpleNamespace'>[n=20]
            .UF_reds: [n=2]: [[n=4]: (1, 1, 1.25, 1),
                              [n=4]: (0, 1, 1.25, 1)]
            .Vars   : <class 'dict'>[n=3]
                0  : <class 'dict'>[n=1]
                100: <class 'dict'>[n=3]
                500: <class 'dict'>[n=4]

    PP(DR.Vars, 2):

    .. code-block:: none

        <class 'dict'>[n=3]
            0  : <class 'dict'>[n=1]
                'Tnode4': float64 ndarray 732 elems: (3, 977)
            100: <class 'dict'>[n=3]
                'ifatm' : float64 ndarray 46896 elems: (48, 977)
                'ifltma': float64 ndarray 17586 elems: (18, 977)
                'ifltmd': float64 ndarray 17586 elems: (18, 977)
            500: <class 'dict'>[n=4]
                'scatm' : float64 ndarray 261836 elems: (268, 977)
                'scdtmd': float64 ndarray 84999 elems: (87, 977)
                'scltma': float64 ndarray 142642 elems: (146, 977)
                'scltmd': float64 ndarray 142642 elems: (146, 977)

    In that example, all the ``DR.Vars`` variables except 'Tnode4'
    have been multiplied by the appropriate ULVS matrix in the call to
    :func:`add`. That is, the SE 100 and 500 matrices all came from
    the ``DR_Def['_vars'].drms`` entry and none came from the
    ``DR_Def['_vars'].nondrms`` entry. The SE 0 matrix 'Tnode4' could
    come from either the `.drms` or `.nondrms` entry.
    """

    def __repr__(self):
        cats = ", ".join(f"'{name}'" for name in self.Info)
        return (
            f"{type(self).__name__} ({hex(id(self))}) with "
            f"{len(self.Info)} categories: [{cats}]"
        )

    def __init__(self):
        """
        Initializes the attributes `Info`, `UF_reds`, and `Vars` to
        empty values.

        The attributes are filled by calls to :func:`add`.
        """
        self.Info = OrderedDict()
        self.UF_reds = []
        self.Vars = {}

    def add(self, nas, drdefs, uf_reds=None, method="replace"):
        """
        Add data recovery definitions for an event or set of modes.

        Parameters
        ----------
        nas : dictionary
            This is the nas2cam dictionary:
            ``nas = pyyeti.nastran.op2.rdnas2cam()``. Only used if at
            least one category in `drdefs` is for an upstream
            superelement (se != 0) and has a data recovery matrix. Can
            be anything (like None) if not needed.
        drdefs : :class:`DR_Def` instance or None
            Contains the data recovery definitions for, typically, one
            superelement. See :class:`DR_Def`. If None, this routine
            does nothing.
        uf_reds : 4-element tuple or None; optional
            If not None, this is the uncertainty factors in "reds"
            order: [rigid, elastic, dynamic, static]. The values in
            `uf_reds` either replace or multiply the original values
            (see `method`). Use a value of None for a particular
            uncertainty value to retain the original value
            unmodified. This `uf_reds` option can be useful when
            uncertainty factors are event specific rather than data
            recovery category specific or you need to add in a forcing
            function uncertainty factor.

            For example, to reset the dynamic uncertainty factor to
            1.1 while leaving the other values unchanged::

                uf_reds=(None, None, 1.1, None)
                DR.add(nas, drdefs, uf_reds)

            For another example, to increase the rigid-body and
            elastic uncertainty factors by a factor of 1.05 while
            leaving the other two values unchanged::

                uf_reds=(1.05, 1.05, None, None)
                DR.add(nas, drdefs, uf_reds, method='multiply')

        method : string or function (callable); optional
            Specifies how to update the "uf_reds" settings:

              ============  ========================================
                `method`                 Description
              ============  ========================================
              'replace'     Values in `uf_reds` (that are not None)
                            replace old values.
              'multiply'    Values in `uf_reds` (that are not None)
                            multiply the old values.
               callable     Values are computed by function (or any
                            callable). The function is only called
                            for entries where `uf_reds` is not None.
                            The call is:
                            ``method(old_value, new_value)``. See
                            examples below.
              ============  ========================================

        Notes
        -----
        Typically called once for each superelement where data
        recovery is requested. The attributes `Info`, `UF_reds` and
        `Vars` are all updated on each call to this routine.

        See :class:`DR_Def` for a discussion about how the order of
        data recovery is determined. In summary: :func:`DR_Event.add`
        determines the order of :class:`DR_Def` instances, and
        :func:`DR_Def.add` determines the order of data recovery
        categories within each :class:`DR_Def` instance.
        :func:`DR_Event.set_dr_order` can be used to modify the final
        order.

        Following are some examples of providing a function for the
        `method` parameter. Note that the function is only called when
        the `uf_reds` value is not None.

        These two calls are equivalent::

            DR.add(nas, drdefs, uf_reds, 'replace')
            DR.add(nas, drdefs, uf_reds, lambda old, new: new)

        These are also equivalent::

            DR.add(nas, drdefs, uf_reds, 'multiply')
            DR.add(nas, drdefs, uf_reds, lambda old, new: old*new)

        As a final example, if you wanted to add values onto the
        previous settings instead of multiply, you could do this::

            DR.add(nas, drdefs, uf_reds, lambda old, new: old+new)

        Raises
        ------
        ValueError
            When the there are duplicate category names.
        """
        if drdefs is None:
            return

        for name, drminfo in drdefs.items():
            if name == "_vars":
                continue

            try:
                active = drminfo.active
            except AttributeError:
                active = "yes"

            if active != "yes":
                continue

            if name in self.Info:
                raise ValueError(f'"{name}" data recovery category already defined')

            # variables for how to do data recovery:
            self.Info[name] = copy.copy(drdefs[name])

            # reset uf_reds if input:
            if uf_reds is not None:
                self.Info[name].uf_reds = _merge_uf_reds(
                    self.Info[name].uf_reds, uf_reds, method=method
                )

            # collect all sets of uncertainty factors together for the
            # apply_uf routine later:
            uf_reds_cur = self.Info[name].uf_reds
            if uf_reds_cur not in self.UF_reds:
                self.UF_reds.append(uf_reds_cur)

        se_last = -2
        # apply ULVS to all drms and put in DR:
        for se, dct in drdefs["_vars"].drms.items():
            if not dct:
                continue
            if se not in self.Vars:
                self.Vars[se] = {}
            if se not in (0, se_last):
                ulvs = nas["ulvs"][se]
                uset = nas["uset"][se]
                # Want bset partition from aset. But note that in the
                # .asm, .pch approach to SE's, it is valid in Nastran
                # to just put all b-set & q-set in a generic a-set.
                # If that's the case, find q-set by finding the
                # spoints:
                bset = n2p.mksetpv(uset, "a", "b")  # bool type
                if bset.all():
                    # manually check for q-set in the a-set:
                    aset = np.nonzero(n2p.mksetpv(uset, "p", "a"))[0]
                    dof = uset.index.get_level_values("dof")[aset]
                    qset = dof == 0  # spoints
                    bset = ~qset
                bset = np.nonzero(bset)[0]
                Lb = len(bset)
            se_last = se

            for name, mat in dct.items():
                if name in self.Vars[se]:
                    raise ValueError(f'"{name}" is already in Vars[{se}]')
                if se == 0:
                    self.Vars[se][name] = mat
                elif mat.shape[1] > Lb:
                    self.Vars[se][name] = mat @ ulvs
                else:
                    self.Vars[se][name] = mat @ ulvs[bset]

        # put all nondrms in DR:
        for se, dct in drdefs["_vars"].nondrms.items():
            if se not in self.Vars:
                self.Vars[se] = {}
            for name, mat in dct.items():
                if name in self.Vars[se]:
                    raise ValueError(f'"{name}" is already in Vars[{se}]')
                self.Vars[se][name] = mat

    def set_dr_order(self, cats, where):
        """
        Set a new data recovery order

        Parameters
        ----------
        cats : iterable
            Iterable of category names in the ordered desired for data
            recovery. Not all categories need to be included, just
            those where a new order is desired. For example, if
            "scltm" must be done before "scltm2", then ``cats =
            ('scltm', 'scltm2')`` is sufficient.
        where : string
            Either 'first' or 'last'. Specifies where to put the
            reordered categories in the final order.

        Notes
        -----
        This is a convenience method for the
        :func:`pyyeti.ytools.reorder_dict` routine.  Updates the
        `Info` attribute to reflect the new order. Call this routine
        before calling :func:`prepare_results`.

        See :class:`DR_Def` for a discussion about how the order of
        data recovery is determined. In summary: :func:`DR_Event.add`
        determines the order of :class:`DR_Def` instances, and
        :func:`DR_Def.add` determines the order of data recovery
        categories within each :class:`DR_Def` instance.  This routine
        can be used to modify the final order.

        Raises
        ------
        ValueError
            If an item in `cats` is not currently in `self.Info`
        ValueError
            If `where` is not 'first' or 'last'

        Examples
        --------
        Build a minimal instance of :class:`DR_Event` incorporating
        two :class:`DR_Def` instances so that
        :func:`DR_Event.set_dr_order` can be fully demonstrated. This
        also demonstrates the use of :func:`DR_Def.add` without using
        the :func:`DR_Def.addcat` decorator.

        >>> from pyyeti import cla
        >>>
        >>> drdefs0 = cla.DR_Def()
        >>> for name, nrows in (('atm0', 12),
        ...                     ('ltm0', 30),
        ...                     ('dtm0', 9)):
        ...     drdefs0.add(name=name, labels=nrows, drfunc='no func')
        >>>
        >>> drdefs1 = cla.DR_Def()
        >>> for name, nrows in (('atm1', 12),
        ...                     ('ltm1', 30),
        ...                     ('dtm1', 9)):
        ...     drdefs1.add(name=name, labels=nrows, drfunc='no func')
        >>>
        >>> DR = cla.DR_Event()
        >>> DR.add(None, drdefs1)
        >>> DR.add(None, drdefs0)

        Show that original order is as defined (`drdefs1` is first):

        >>> print(repr(DR))    # doctest: +ELLIPSIS
        DR_Event ... ['atm1', 'ltm1', 'dtm1', 'atm0', 'ltm0', 'dtm0']

        For demonstration, put the two :class:`DR_Def` instances in a
        different order:

        >>> DR = cla.DR_Event()
        >>> DR.add(None, drdefs0)
        >>> DR.add(None, drdefs1)
        >>> print(repr(DR))    # doctest: +ELLIPSIS
        DR_Event ... ['atm0', 'ltm0', 'dtm0', 'atm1', 'ltm1', 'dtm1']

        Ensure that 'ltm1', 'dtm0', 'atm1' are recovered in that
        order, and assume the others are okay in current order:

        Case 1: put 'ltm1', 'dtm0', 'atm1' first:

        >>> DR.set_dr_order(('ltm1', 'dtm0', 'atm1'), where='first')
        >>> print(repr(DR))    # doctest: +ELLIPSIS
        DR_Event ... ['ltm1', 'dtm0', 'atm1', 'atm0', 'ltm0', 'dtm1']

        Case 2: put 'ltm1', 'dtm0', 'atm1' last:

        >>> DR.set_dr_order(('ltm1', 'dtm0', 'atm1'), where='last')
        >>> print(repr(DR))    # doctest: +ELLIPSIS
        DR_Event ... ['atm0', 'ltm0', 'dtm1', 'ltm1', 'dtm0', 'atm1']
        """
        self.Info = reorder_dict(self.Info, cats, where)

    def prepare_results(self, mission, event):
        """
        Returns an instance of the :class:`DR_Results` class.

        Parameters
        ----------
        mission : str
            Identifies the CLA
        event : str
            Name of event

        Returns
        -------
        results : :class:`DR_Results` instance
            Subclass of dict containing categories with results (see
            :class:`DR_Results`).

        Notes
        -----
        Uses the `Info` attribute (see :class:`DR_Event`) and calls
        :func:`DR_Results.init` to build the initial results data
        structure for all data recovery categories.
        """
        results = DR_Results()
        results.init(self.Info, mission, event)
        return results

    def apply_uf(self, sol, m, b, k, nrb, rfmodes):
        """
        Applies the uncertainty factors to the modal ODE solution

        Parameters
        ----------
        sol : SimpleNamespace
            Solution, input only; expected to have::

                .a = modal acceleration time-history matrix
                .v = modal velocity time-history matrix
                .d = modal displacement time-history matrix
                .pg = g-set forces; optional

        m : 1d or 2d ndarray or None
            Modal mass; can be vector or matrix or None (for identity)
        b : 1d or 2d ndarray
            Modal damping; vector or matrix
        k : 1d or 2d ndarray
            Modal stiffness; vector or matrix
        nrb : scalar
            Number of rigid-body modes
        rfmodes : index vector or None
            Specifies where the res-flex modes are; if None, no
            resflex

        Returns
        -------
        solout : dict
            Dictionary of solution namespaces with scaled versions
            of `.a`, `.v`, `.d` and `.pg`. The keys are all the
            "uf_reds" values. Additionally, the displacement member is
            separated into static and dynamic parts: `.d_static`,
            `.d_dynamic`. On output, ``.d = .d_static + .d_dynamic``.
            For example, if one of the "uf_reds" tuples is:
            ``(1, 1, 1.25, 1)``, then these variables will exist::

                solout[(1, 1, 1.25, 1)].a
                solout[(1, 1, 1.25, 1)].v
                solout[(1, 1, 1.25, 1)].d
                solout[(1, 1, 1.25, 1)].d_static
                solout[(1, 1, 1.25, 1)].d_dynamic
                solout[(1, 1, 1.25, 1)].pg (optional)

        Notes
        -----
        Uncertainty factors are applied as follows (rb=rigid-body,
        el=elastic, rf=residual-flexibility)::

           ruf = rb uncertainty factor
           euf = el uncertainty factor
           duf = dynamic uncertainty factor
           suf = static uncertainty factor

           .a_rb and .v_rb - scaled by ruf*suf
           .a_el and .v_el - scaled by euf*duf
           .a_rf and .v_rf - zeroed out

           .d_rb - zeroed out
           .d_el - static part:  scaled by euf*suf
                 - dynamic part: scaled by euf*duf
           .d_rf - scaled by euf*suf

           .pg   - scaled by suf

        Note that d_el is written out as::

              d_el = euf*inv(k_el)*(suf*F_el - duf*(a_el+b_el*v_el))

        where::

              F = m*a + b*v + k*d
        """
        n = k.shape[0]
        use_velo = True

        # genforce = m*a + b*v + k*d
        def _comp_genforce(sol, d):
            if m is None:
                genforce = sol.a.copy()
            elif m.ndim == 1:
                genforce = m[:, None] * sol.a
            else:
                genforce = m @ sol.a

            if b.ndim == 1:
                genforce += b[:, None] * sol.v
            else:
                genforce += b @ sol.v

            if k.ndim == 1:
                genforce += k[:, None] * d
            else:
                genforce += k @ d
            return genforce

        solout = {}
        # This routine will do its work in two loops:
        # - a copy loop
        # - an apply ufs loop
        # The copy loop is separate to be efficient, since copying
        # from 'F' order to 'C' order is slower than 'C' to 'C'
        last = None
        for item in self.UF_reds:
            if last:
                solout[item] = copy.deepcopy(last)
            else:
                # we want C contiguous a, v, d variables for faster uf
                # application
                # - variable 'd' is skipped because it is created
                #   below
                solout[item] = SimpleNamespace()
                for name, value in vars(sol).items():
                    if name == "d":
                        continue
                    try:
                        valcopy = value.copy()
                    except AttributeError:
                        valcopy = copy.deepcopy(value)
                    setattr(solout[item], name, valcopy)
                last = solout[item]
                genforce = _comp_genforce(last, sol.d)

        for item in self.UF_reds:
            ruf, euf, duf, suf = item
            SOL = solout[item]
            SOL.d_static = np.empty_like(SOL.a)
            SOL.d_dynamic = np.empty_like(SOL.a)

            # apply ufs:
            if nrb > 0:
                SOL.a[:nrb] *= ruf * suf
                SOL.v[:nrb] *= ruf * suf
                SOL.d_static[:nrb] = 0.0
                SOL.d_dynamic[:nrb] = 0.0

            if rfmodes is not None:
                SOL.a[rfmodes] = 0.0
                SOL.v[rfmodes] = 0.0

            try:
                SOL.pg *= suf
            except AttributeError:
                pass

            if nrb < n:
                SOL.a[nrb:] *= euf * duf
                SOL.v[nrb:] *= euf * duf

                if m is None:
                    avterm = SOL.a[nrb:].copy()
                elif m.ndim == 1:
                    avterm = m[nrb:, None] * SOL.a[nrb:]
                else:
                    avterm = m[nrb:, nrb:] @ SOL.a[nrb:]

                if not use_velo:  # pragma: no cover
                    msg = (
                        "not including velocity term in mode-"
                        "acceleration formulation for "
                        "displacements."
                    )
                    warnings.warn(msg, RuntimeWarning)
                else:
                    if b.ndim == 1:
                        avterm += b[nrb:, None] * SOL.v[nrb:]
                    else:
                        avterm += b[nrb:, nrb:] @ SOL.v[nrb:]

                # in case there is mass coupling between rfmodes and
                # other modes
                if rfmodes is not None:
                    avterm[rfmodes - nrb] = 0.0

                gf = (euf * suf) * genforce[nrb:]
                if k.ndim == 1:
                    invk = (1 / k[nrb:])[:, None]
                    SOL.d_static[nrb:] = invk * gf
                    SOL.d_dynamic[nrb:, :] = -invk * avterm
                else:
                    lup = la.lu_factor(k[nrb:, nrb:])
                    SOL.d_static[nrb:] = la.lu_solve(lup, gf)
                    SOL.d_dynamic[nrb:, :] = la.lu_solve(lup, -avterm)

                SOL.d = SOL.d_static + SOL.d_dynamic
        return solout

    def frf_apply_uf(self, sol, nrb):
        """
        Applies the uncertainty factors to the frequency response
        functions (FRFs).

        Parameters
        ----------
        sol : SimpleNamespace
            Solution, input only; expected to have::

                .a = modal acceleration FRF matrix
                .v = modal velocity FRF matrix
                .d = modal displacement FRF matrix
                .pg = g-set forces; optional

        nrb : scalar
            Number of rigid-body modes

        Returns
        -------
        solout : dict
            Dictionary of solution namespaces with scaled versions of
            `.a`, `.v`, `.d` and `.pg`. The keys are all the "uf_reds"
            values. For example, if one of the "uf_reds" tuples is:
            ``(1, 1, 1.25, 1)``, then these variables will exist::

                solout[(1, 1, 1.25, 1)].a
                solout[(1, 1, 1.25, 1)].v
                solout[(1, 1, 1.25, 1)].d
                solout[(1, 1, 1.25, 1)].pg (optional)

        Notes
        -----
        Uncertainty factors are applied as follows (rb=rigid-body,
        el=elastic, rf=residual-flexibility)::

           ruf = rb uncertainty factor
           euf = el uncertainty factor
           duf = dynamic uncertainty factor
           suf = static uncertainty factor

           .a_rb, .v_rb, d_rb - scaled by ruf*suf
           .a_el, .v_el, d_el - scaled by euf*duf
           .pg   - scaled by suf
        """
        solout = {}
        for item in self.UF_reds:
            ruf, euf, duf, suf = item
            solout[item] = copy.deepcopy(sol)
            SOL = solout[item]
            SOL.a[:nrb] *= ruf * suf
            SOL.v[:nrb] *= ruf * suf
            SOL.d[:nrb] *= ruf * suf
            SOL.a[nrb:] *= euf * duf
            SOL.v[nrb:] *= euf * duf
            SOL.d[nrb:] *= euf * duf
            if "pg" in SOL.__dict__:
                SOL.pg *= suf
        return solout

    def get_Qs(self):
        """
        Get list of all unique Q's used for SRS in all categories

        Returns
        -------
        Qs : list
            list of all unique Q's used for SRS in all categories
        """
        Qs = set()
        for v in self.Info.values():
            if v.srsQs is not None:
                Qs |= set(v.srsQs)  # or: Qs = Qs.union(v.srsQs)
        return sorted(Qs)
