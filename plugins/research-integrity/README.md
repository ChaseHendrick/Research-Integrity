# Research integrity

Instructions for an assistant that is searching literature, checking a proof, running a numerical argument, or preparing a preprint. The plugin is one skill, `skills/research-integrity/SKILL.md`. It does not run a server, a hook, or a script. It does not send data anywhere, and it does not fetch pages on its own.

What Claude does with it: when the work is a research claim, Claude follows the skill. A claim is labelled with how it is known. A source that did not load is not written down as "nothing found." A check is not called passed unless it can fail. An in-project reading is not called peer review.

What it does not do: it does not open a network connection, store an account, or read a credential. Anything Claude reads is a file you already asked it to work on in that conversation. Uninstalling the skill removes the instructions. There is no separate copy of your work.

The rules come from a public record of 80 failures in one research project. That record is evidence for the rules. It is not a claim that following the skill removes errors, and this plugin is not an Anthropic product.
