# RC-67 batch window

Receipt packages include final receipt rows for a half-open package window. The
window is normally expressed using the receipt's visible `created_at` timestamp.

Late acknowledgements and partner replays may attach additional timestamps. When
those values are present, release-room checks compare package contents against
the timestamp that best represents when the row became visible to the partner.
