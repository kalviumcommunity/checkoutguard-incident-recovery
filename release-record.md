# Supplied simulated release record (not observed production history)
2026.10.1: known-good checkout release; inventory adapter configuration compatible.
2026.10.2: current release; inventory adapter configuration changed; checkout requests fail.
Both variants are bundled in this local teaching image. RELEASE selects the variant. Changing RELEASE recreates the service; it is a local release-selector rollback, not a registry image rollback.
No real customers, production incident or cloud deployment exist in this exercise.
