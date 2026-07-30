schema_version: '1.0'
selection_lock_sha256: 4f887209c102963fd6096c265fdfd6cae60de9ab23469c2dfebe5a8bed0565eb
selection_result_sha256: 9106d31402ad9aa42cefed3189a3922873c83c9f2dac89b0ba6368098bd302d6
selected:
- id: foundation.system-boundaries
  path: foundations/system-boundaries.md
  sha256: a326964ec74303e0f08f3e7207e4836a0ff04c93c7f8516e6190b47925ec06db
  priority: required
  reasons:
  - Required foundation or lens for project-architecture-audit.
  - 'Task matches trigger(s): contract'
- id: domain.plugin-platform
  path: domains/plugin-platform/overview.md
  sha256: b72a0e3b6959464b32c9a4d44b50baa40b4baf13b5b14f65f99d094f301bf58c
  priority: required
  reasons:
  - Project profile or detected facts require plugin-platform.
  - 'Task matches trigger(s): plugin'
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
- id: domain.test-automation-platform
  path: domains/test-automation-platform/overview.md
  sha256: 7ce2621239bad831f4a6689a1718b5dd1cdbbf1d6d2e3bb9a6d043457a70e016
  priority: required
  reasons:
  - Project profile or detected facts require test-automation-platform.
- id: anti-pattern.multi-agent-for-workflow
  path: anti-patterns/multi-agent-for-workflow.md
  sha256: c38a11b01e023d1ec78ebae148ff36a3edba3dd6d8b561610954c4c54e3a4421
  priority: recommended
  reasons:
  - 'Task matches trigger(s): workflow'
- id: case-study.queue-worker-before-workflow
  path: case-studies/queue-worker-before-workflow.md
  sha256: c136b2d15ee59068b4c14f3d8bbb5d044f01df369ed867f97f2b62266551bd30
  priority: recommended
  reasons:
  - 'Task matches trigger(s): workflow'
- id: decision.optimistic-vs-pessimistic-update
  path: decision-guides/optimistic-vs-pessimistic-update.md
  sha256: 935e92047bb3a9ce3b4ba8484b5cecc28c5c981a1c61453aff31bb892854ff64
  priority: recommended
  reasons:
  - 'Task matches trigger(s): rollback'
- id: decision.workflow-vs-agent
  path: decision-guides/workflow-vs-agent.md
  sha256: f8fc79dfd6cbe7824c9bafe120e116dd1e7c681dd84f27806dbed4bf5bf9b36d
  priority: recommended
  reasons:
  - 'Task matches trigger(s): workflow'
- id: foundation.architecture-principles
  path: foundations/architecture-principles.md
  sha256: 9394a24578d7e7ec483c68ab78bfe6192451411552ee92401744b7e87e56ca1f
  priority: recommended
  reasons:
  - 'Task matches trigger(s): boundary'
