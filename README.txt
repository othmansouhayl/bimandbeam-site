Fixes the invisible CTA button text bug: the green "Get the free preview" /
"Get the checklist" buttons inside article content had black text hidden
behind a more specific green-link rule from the dark-theme override. Fixed
with a targeted !important on the button's own color rule.

This patch only touches wp-content/brand.css - just overwrite that one file
in your repo, commit, push. Affects every article page since they all share
this single stylesheet.
