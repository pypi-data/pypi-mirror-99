Defining Single Station Observations and Observation Metadata
=============================================================

Session Definition Files
------------------------
.. automodule:: lsl.common.sdf

Session Structure
+++++++++++++++++
:mod:`lsl.common.sdf` (DP-based stations) and :mod:`lsl.common.sdfADP` (ADP-based stations) provide means to represent a set of observations as Python objects.  For each
:class:`lsl.common.sdf.Project`, there is:

  1) An observer (:class:`lsl.common.sdf.Observer`)
  2) The project office comments (:class:`lsl.common.sdf.ProjectOffice`)
  3) A single session that defines the SDF (:class:`lsl.common.sdf.Session`)
  
The session contains one or more observerions (:class:`lsl.common.sdf.Observation`).  Each observing mode supported
by the LWA is sub-classed (see below).

.. autoclass:: lsl.common.sdf.Project
   :members:
.. autoclass:: lsl.common.sdf.Observer
   :members:
.. autoclass:: lsl.common.sdf.ProjectOffice
   :members:
.. autoclass:: lsl.common.sdf.Session
   :members:
.. autoclass:: lsl.common.sdf.Observation
   :members:

Observing Modes
+++++++++++++++
.. autoclass:: lsl.common.sdf.TBW
   :members:
.. autoclass:: lsl.common.sdf.TBN
   :members:
.. autoclass:: lsl.common.sdf.DRX
   :members:
.. autoclass:: lsl.common.sdf.Solar
   :members:
.. autoclass:: lsl.common.sdf.Jovian
   :members:
.. autoclass:: lsl.common.sdf.Stepped
   :members: 
.. autoclass:: lsl.common.sdf.BeamStep
   :members:

MCS Metadata Tarball Utilities
------------------------------
.. automodule:: lsl.common.metabundle
   :members:

Supporting Functions
--------------------

Conversion to/from MJD and MPM
++++++++++++++++++++++++++++++
These functions convert Python datetime instances to modified Julian Data (MJD) and
milliseconds past midnight (MPM) pairs.

.. autofunction:: lsl.common.mcs.datetime_to_mjdmpm
.. autofunction:: lsl.common.mcs.mjdmpm_to_datetime

Specifiying Delay and Gains for the Digital Processor
+++++++++++++++++++++++++++++++++++++++++++++++++++++
These functions are intended to help define observations that are run in Stepped mode with 
the beamforming method set to "SPEC_DELAYS_GAINS".

.. autofunction:: lsl.common.mcs.delay_to_mcsd
.. autofunction:: lsl.common.mcs.mcsd_to_delay
.. autofunction:: lsl.common.mcs.gain_to_mcsg
.. autofunction:: lsl.common.mcs.mcsg_to_gain

Interpretting MCS Numeric Codes
+++++++++++++++++++++++++++++++
These functions convert various MCS numeric codes found in the metatdata into strings.

.. autofunction:: lsl.common.mcs.status_to_string
.. autofunction:: lsl.common.mcs.summary_to_string
.. autofunction:: lsl.common.mcs.sid_to_string
.. autofunction:: lsl.common.mcs.cid_to_string
.. autofunction:: lsl.common.mcs.mode_to_string

