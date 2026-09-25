# Technical validator revision

The first technical run passed 46 of 48 checks. Two failures were validator assumptions, not findings against the historical text: it treated evidence strings containing candidate IDs or multiple filenames as single filesystem paths, and it expected the unresolved-only ledger to include the three resolved entries.

Revision 2 parses each named evidence file while retaining candidate labels in the original ledger. It checks that the unresolved ledger is exactly the current apparatus with `RESOLVED_RETAINED` entries excluded. The historical transcription, apparatus decisions, PDF builds, and image assets were not changed for these validator repairs. The first result and script are preserved here.

Both versions are technical programs written by the producing assistant, not independent philological auditors.
