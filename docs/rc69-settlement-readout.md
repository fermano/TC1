# RC-69 settlement readout

RC-69 package checks have two separate layers:

1. row eligibility: posted or settled settlement rows are included once per tenant, settlement id, and package type;
2. artifact identity: release promotion uses only manifests built from the current release branch.

A package can have the expected row count and still remain held if its manifest was built from a preview or handoff branch. Release notes should state both the row readout and the source ref/commit used to build the artifact.
