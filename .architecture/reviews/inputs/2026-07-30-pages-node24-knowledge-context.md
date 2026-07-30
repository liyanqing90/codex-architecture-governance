schema_version: '1.0'
selection_lock_sha256: 2e0ea697c535db3a18188e40e0c2c1c6b9966724b9182628e2f7284def3baee3
selection_result_sha256: b5327d16f217b61b28e13450abe132409a24bfe0ea242a27329caed07c312c53
selected:
- id: foundation.compatibility
  path: foundations/compatibility.md
  sha256: 17d8e8c8557969246fe2e9a62e8a645aeac171c9c9d2cbeb5d0bdfc27e51330b
  priority: required
  reasons:
  - Explicit caller include.
  - 'Task matches trigger(s): compatibility'
- id: foundation.data-ownership
  path: foundations/data-ownership.md
  sha256: 260f240ec9782f5a42a68481652912532cfcd6a0b07fdc5366d44388cc3d0204
  priority: required
  reasons:
  - Required foundation or lens for project-architecture-audit.
- id: foundation.evidence-reasoning
  path: foundations/evidence-reasoning.md
  sha256: e3c370e04b8a9be5e64ea0d107281043652b1cdba3393fb61b57efd77262650f
  priority: required
  reasons:
  - Required foundation or lens for project-architecture-audit.
- id: foundation.proportional-design
  path: foundations/proportional-design.md
  sha256: ccfa63d523fab3503c47dbf73fc7a9ae85c7fc516856bcf422322c0d92a409df
  priority: required
  reasons:
  - Required foundation or lens for project-architecture-audit.
- id: foundation.quality-attributes
  path: foundations/quality-attributes.md
  sha256: 50d92ab7563d70605408ba4592d9445f79f6eb0cecb50195471b56e42418b680
  priority: required
  reasons:
  - Required foundation or lens for project-architecture-audit.
- id: foundation.system-boundaries
  path: foundations/system-boundaries.md
  sha256: a326964ec74303e0f08f3e7207e4836a0ff04c93c7f8516e6190b47925ec06db
  priority: required
  reasons:
  - Required foundation or lens for project-architecture-audit.
- id: domain.plugin-platform
  path: domains/plugin-platform/overview.md
  sha256: b72a0e3b6959464b32c9a4d44b50baa40b4baf13b5b14f65f99d094f301bf58c
  priority: required
  reasons:
  - Project profile or detected facts require plugin-platform.
- id: domain.test-automation-platform
  path: domains/test-automation-platform/overview.md
  sha256: 7ce2621239bad831f4a6689a1718b5dd1cdbbf1d6d2e3bb9a6d043457a70e016
  priority: required
  reasons:
  - Project profile or detected facts require test-automation-platform.
