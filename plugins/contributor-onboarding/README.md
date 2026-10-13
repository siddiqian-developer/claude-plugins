# contributor-onboarding

Say **"onboard me"** in a repository and Claude sets the clone up the way the
*project* says, not the way this plugin assumes.

The project declares its setup in `.claude/onboarding.md`:

```markdown
# Onboarding

- Report: `scripts/setup-clone.sh --check`
- Apply: `scripts/setup-clone.sh --role "<role>" --install`
- Ask for: the person's role (never their name)
- From another person: host access and credentials, sent by the maintainer over a private channel
- Next: docs/TUTORIAL.md
```

Without that file it falls back to the setup section of `CONTRIBUTING.md` or
`README.md`, then to a `scripts/setup*.sh`. It always reports before changing
anything, never writes a secret into a tracked file, and never asks for a
credential in the conversation.

## Install, for a whole team

Commit to the repository's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "siddiqian-plugins": { "source": { "source": "github", "repo": "siddiqian-developer/claude-plugins" } }
  },
  "enabledPlugins": { "contributor-onboarding@siddiqian-plugins": true }
}
```
