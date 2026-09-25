#!/usr/bin/env python3
"""Inserts one natural, contextual, dofollow backlink to bimaturity.app into the
main entry-content of each mapped legacy BIM/Revit article (same owner, topically
relevant cross-promotion). Idempotent: skips files that already contain the
bb-bl-link marker class."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER_CLASS = "bb-bl-link"

OPEN_MARK = "entry-content single-content"
CLOSE_MARK = "<!-- .entry-content -->"

LINK = '<a class="{cls}" href="{url}" target="_blank" rel="noopener">{anchor}</a>'.format

# (file relative path, sentence template with {LINK} placeholder)
PAGES = [
    ("2022/08/how-to-become-bim-manager-in-5-steps/index.html",
     "https://bimaturity.app/en/blog/signes-coordinateur-bim-pret-devenir-manager",
     "the concrete signs you're ready to become a BIM manager",
     "If you're a coordinator eyeing that jump, it's worth checking {LINK} before you make the leap."),

    ("2022/12/how-to-become-a-bim-coordinator/index.html",
     "https://bimaturity.app/en/blog/definir-niveaux-competence-bim-junior-senior",
     "this breakdown of junior vs. senior BIM competency levels",
     "Before you apply, it helps to know exactly where your BIM skills currently sit — {LINK} is a useful benchmark."),

    ("2022/12/iso-19650-bim-steps-of-implementation/index.html",
     "https://bimaturity.app/en/blog/eir-bep-cde-comprendre-iso-19650",
     "this plain-language guide to EIR, BEP, and CDE under ISO 19650",
     "If terms like EIR, BEP, and CDE still feel fuzzy, {LINK} fills in the gaps."),

    ("2025/04/avenir-bim-manager-competences-cles/index.html",
     "https://bimaturity.app/blog/signes-coordinateur-bim-pret-devenir-manager",
     "les signes concrets qu'un coordinateur BIM est prêt à devenir manager",
     "Avant de sauter le pas, ça vaut le coup de vérifier {LINK}."),

    ("2025/04/ids-bim-validation-ifc/index.html",
     "https://bimaturity.app/blog/eir-bep-cde-comprendre-iso-19650",
     "ce guide sur l'EIR, le BEP et la CDE",
     "Ce chapitre s'inscrit dans une logique plus large de conformité ISO 19650 — {LINK} remet ces exigences en contexte."),

    ("2021/09/bim-rolesandresponsibilities-html/index.html",
     "https://bimaturity.app/en/blog/definir-niveaux-competence-bim-junior-senior",
     "this framework for defining junior vs. senior BIM skill levels",
     "Mapping who does what is only half the picture — {LINK} helps put a number on where each role actually stands."),

    ("2022/01/bim-vs-vdc-similarities-and-differences-html/index.html",
     "https://bimaturity.app/en/blog/maturite-bim-ne-se-mesure-pas-quaux-outils",
     "maturity isn't just about which tool you pick",
     "Whatever label you use, the real question is how mature your BIM process actually is — and {LINK}."),

    ("2022/07/revit-courses-bim-courses/index.html",
     "https://bimaturity.app/en/blog/definir-niveaux-competence-bim-junior-senior",
     "this junior-to-senior BIM skill breakdown",
     "Picking the right course is easier once you know which competency level you're actually training toward — {LINK} is a useful reference."),

    ("2025/07/global-bim-arket-is-exploding/index.html",
     "https://bimaturity.app/en/blog/maturite-bim-ne-se-mesure-pas-quaux-outils",
     "maturity isn't just about the tools in your stack",
     "That growth is pushing firms to formalize how they measure BIM maturity internally, rather than assuming it — a reminder that {LINK}."),

    ("2022/12/bim-for-mep-a-comprehensive-guide/index.html",
     "https://bimaturity.app/en",
     "BIM skills assessment platform",
     "As MEP teams lean harder on BIM, firms are increasingly formalizing how they assess that competency — a {LINK} exists for exactly that."),

    ("2021/09/bim-workflow-vs-cad-workflow-html/index.html",
     "https://bimaturity.app/en",
     "formal BIM maturity assessment",
     "That shift in workflow is also a shift in the skills a team needs — which is why more firms now run a {LINK} rather than assuming everyone's on the same page."),

    ("2021/09/what-is-bim-what-are-its-benefits-and-html/index.html",
     "https://bimaturity.app/en",
     "BIMaturity's assessment platform",
     "Once a firm buys into BIM, the next question is usually how mature its own process really is — that's the gap {LINK} is built to close."),

    # Job post articles — hiring-context link to the "evaluate candidates objectively" guide, anchors rotated.
    ("2022/11/bim-coordinator-job-post-enermech-ireland/index.html",
     "https://bimaturity.app/en/blog/evaluer-objectivement-modeleur-bim-entretien",
     "evaluating a BIM candidate's real skill level objectively in an interview",
     "If you're the one doing the hiring for a role like this, {LINK} is worth reading before the next round."),

    ("2022/11/bim-coordinator-job-post-pm-group-ireland/index.html",
     "https://bimaturity.app/en/blog/evaluer-objectivement-modeleur-bim-entretien",
     "evaluate BIM candidates objectively in interviews",
     "Sorting genuine BIM skill from a polished CV is hard — here's how to {LINK}."),

    ("2022/11/bim-coordinator-job-post-richard-kennedy-architects-usa/index.html",
     "https://bimaturity.app/en/blog/evaluer-objectivement-modeleur-bim-entretien",
     "structuring a BIM interview around objective criteria",
     "Before extending an offer, it's worth {LINK} rather than gut feel."),

    ("2022/11/bim-coordinator-job-post-stc-group-ireland/index.html",
     "https://bimaturity.app/en/blog/evaluer-objectivement-modeleur-bim-entretien",
     "objectively evaluating a candidate's BIM skills at interview stage",
     "For firms hiring into a role like this, {LINK} tends to save a lot of guesswork."),

    ("2022/11/bim-lead-job-post-enermech-ireland/index.html",
     "https://bimaturity.app/en/blog/evaluer-objectivement-modeleur-bim-entretien",
     "evaluating a BIM candidate's real skill level objectively",
     "A lead role raises the stakes on getting this right — {LINK} in the interview is a good place to start."),

    ("2022/11/bim-manager-job-post-paris-france/index.html",
     "https://bimaturity.app/en/blog/signes-coordinateur-bim-pret-devenir-manager",
     "the concrete signs a coordinator is ready to become a manager",
     "If you're weighing an internal promotion for a role like this, {LINK} is a useful checklist."),

    ("2022/11/bim-manager-job-post-siemens-energy-manchester-england-uk/index.html",
     "https://bimaturity.app/en/blog/evaluer-objectivement-modeleur-bim-entretien",
     "evaluate BIM candidates objectively in interviews",
     "Whether you're hiring externally or promoting from within, it helps to {LINK}."),

    ("2022/11/bim-modeler-job-post-extia-france/index.html",
     "https://bimaturity.app/en/blog/evaluer-objectivement-modeleur-bim-entretien",
     "objectively evaluating a BIM modeler's skill level in an interview",
     "For a modeler role, {LINK} matters more than a portfolio alone."),

    ("2022/11/bim-modeler-job-post-sia-luxembourg/index.html",
     "https://bimaturity.app/en/blog/evaluer-objectivement-modeleur-bim-entretien",
     "objectively evaluating a BIM modeler's skill level in an interview",
     "For a modeler role, {LINK} matters more than a portfolio alone."),

    ("2022/11/bim-specialist-job-post-seattle-usa/index.html",
     "https://bimaturity.app/en/blog/evaluer-objectivement-modeleur-bim-entretien",
     "evaluating a BIM candidate's real skill level objectively",
     "For a specialist role, {LINK} beats relying on years-of-experience alone."),
]


def main():
    placed, skipped, missed = 0, 0, 0
    for rel_path, url, anchor, sentence_tpl in PAGES:
        f = ROOT / rel_path
        if not f.exists():
            print(f"MISSING FILE: {f}")
            missed += 1
            continue

        text = f.read_text(encoding="utf-8")
        if MARKER_CLASS in text:
            skipped += 1
            continue

        open_idx = text.find(OPEN_MARK)
        if open_idx == -1:
            print(f"MISS (no entry-content found): {f}")
            missed += 1
            continue

        close_idx = text.find(CLOSE_MARK, open_idx)
        if close_idx == -1:
            print(f"MISS (no closing marker found): {f}")
            missed += 1
            continue

        # close_idx points at "<!-- .entry-content -->"; the "</div>" immediately precedes it.
        div_close = text.rfind("</div>", open_idx, close_idx)
        if div_close == -1:
            print(f"MISS (no </div> before close marker): {f}")
            missed += 1
            continue

        link_html = LINK(cls=MARKER_CLASS, url=url, anchor=anchor)
        sentence = sentence_tpl.format(LINK=link_html)
        paragraph = f"<p>{sentence}</p>"

        new_text = text[:div_close] + paragraph + text[div_close:]
        f.write_text(new_text, encoding="utf-8")
        placed += 1
        print(f"OK: {rel_path}")

    print(f"\nPlaced: {placed}, already had link: {skipped}, missed: {missed}, total mapped: {len(PAGES)}")


if __name__ == "__main__":
    main()
