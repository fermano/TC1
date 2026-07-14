# Delivery workflow contract

Delivery owner keys are trimmed, lowercased, and collapse runs of Unicode whitespace to a single ASCII space. Punctuation and separators are preserved. Blank owners use `engineering-ops`.

Owner filtering uses the same canonical keys and preserves input record order. A missing owner selection (`owners=None`) means no filtering. An explicitly empty selection (`owners=[]`) returns no records. Duplicate selections never duplicate records.

Delivery summaries expose owner and status. Source metadata may be added as an opt-in field; behavior for blank or missing source values is not yet recorded here.
