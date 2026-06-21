# Evidence Handoff Audit

- Schema: `earnings-call-risk-map.evidence-handoff-audit.v1`
- Package: `earnings-call-risk-map`
- Version: `0.9.3`
- Root: `<redacted-root>`
- Checked artifacts: 93
- Present artifacts: 93
- Missing artifacts: 0
- Source fixtures: 7
- Generated outputs: 78
- Readiness: `ready_with_review`

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Boundaries

- static/local-source only
- no live data
- no broker connection
- no personalized investment advice
- no legal advice
- no accounting advice
- no tax advice
- no buy advice
- no sell advice
- no hold advice

## Checked Artifacts

| Relative path | Role | Present | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| README.md | documentation | yes | 20249 | 433b1445060d5dd9370ba2528b49c3dee8312f1bdd9c2ab1243f9c8be8e2a4fc |
| docs/case-study-limitations.md | freshness_documentation | yes | 4394 | 0a32fc024096b127572c02b86b4ac2529a089aa9e42bffc273bf9707f0f910dd |
| docs/non-advice-boundary.md | source_boundary_documentation | yes | 3689 | 8bd98218315757cd15e9edfe0e59f0f315dc1ac0c5dc96e438312a89ea09fb42 |
| docs/reviewer-evidence.md | reviewer_handoff_documentation | yes | 7267 | 3e0d5b096c8b682acffeda2aaeab16d206cbe2196c7bf201cbf4a329cd6da8b9 |
| docs/security-and-privacy.md | source_boundary_documentation | yes | 3220 | b6829083ba45a2af5ee38e850aefa395c73dbef50e689334dae23613acff3b14 |
| docs/source-attribution-guide.md | source_boundary_documentation | yes | 6714 | 1db47eb6bde1e8264ede9ca93379d136a32e7300d06b9b42dbe513ad54370890 |
| docs/usage.md | documentation | yes | 23277 | 72977f4e2329114a73c432e0053cdf70fd1bd2dffe92e0ed3d6e6fa7de3c9592 |
| examples/input/consumer_hardware.json | source_fixture | yes | 5844 | 7eb3539c44edc2d7e6e1fb3939515b902895bb075002af0f13413a3f1553e08a |
| examples/input/demo_company.json | source_fixture | yes | 2007 | 90a0fa4ae264709ad9648561961a5838d63973c4734d95dcfcdcbef73a8a52a7 |
| examples/input/demo_company_prior.json | source_fixture | yes | 1143 | a2ed62178af4b5ff12213a8b20563a1640771a58db9fbec674e1793ce8c1ef43 |
| examples/input/demo_energy_infrastructure.json | source_fixture | yes | 3943 | 3e26b778eba00846e77772a9bac9b108cc012d408afcf59d032ef3803619cde9 |
| examples/input/public_apple_static_case_study.json | source_fixture | yes | 5809 | 2daa794efd177367d0e454fdcf5681afe9734294030d335954c4e1bc02d649d9 |
| examples/input/sample_filled_template_workflow.json | source_fixture | yes | 5876 | 84aa5f77495087d8780900ec5ab0c94634ffc5067ac877c4dae5433d10365a62 |
| examples/input/semiconductor_equipment.json | source_fixture | yes | 8024 | bc092ff625a9bcd316b17a862c9891bb602ac0b2e138c006f542a300a130b6ce |
| examples/output/agent_workflow.json | generated_json | yes | 4122 | 8a1b74cc4f6d664f830859f141956995393a728608b380becf8fb0ae429664d6 |
| examples/output/agent_workflow.md | generated_markdown | yes | 3426 | ef7fb25f74a4dbcf6416b48bdc67ad3754ac9280adc22dfdeb0af6907a305e1f |
| examples/output/case_study_map.json | generated_json | yes | 6503 | f5b5fd48bf6c271d7d71261eb1be6459e6ea5e59180986df9919f680f3238ac2 |
| examples/output/case_study_map.md | generated_markdown | yes | 5932 | b28540c1fd7b9b58ca211ce9095969dd231df8adca4e1eb308bc8e2efc1347e8 |
| examples/output/command_cheat_sheet.json | generated_json | yes | 4152 | 923c8444bf2d8a0c08d420037b472df2f193b72c945fa94a89204aeadc956725 |
| examples/output/command_cheat_sheet.md | generated_markdown | yes | 2671 | 831e170fc849e685eee7d4f7fa53fb0b85c8d37342243f525d11006003acf0d7 |
| examples/output/command_cheatsheet.json | generated_json | yes | 4152 | 923c8444bf2d8a0c08d420037b472df2f193b72c945fa94a89204aeadc956725 |
| examples/output/command_cheatsheet.md | generated_markdown | yes | 2671 | 831e170fc849e685eee7d4f7fa53fb0b85c8d37342243f525d11006003acf0d7 |
| examples/output/consumer_hardware_dashboard.html | generated_dashboard | yes | 9023 | 4e6915e5f50f18a607e46ff0d05d518c827e1025537b2389e877c4fcfa74131c |
| examples/output/consumer_hardware_report.md | generated_markdown | yes | 4362 | 67710b9d14658ae357725f7f0e42c15dd82ae49cc25823501cd8d6a7e6af1227 |
| examples/output/consumer_hardware_review_queue.json | generated_review_queue | yes | 4338 | e5559de3c425aff7fa2cedf510dbe7f99ee0dc18f150f88e59222a485a8b1498 |
| examples/output/consumer_hardware_review_queue.md | generated_review_queue | yes | 3143 | d5a3c5d64f9446999433a9c64cbda08d6569c8d12b949482cfbd901ca67e4378 |
| examples/output/consumer_hardware_snapshot.json | generated_json | yes | 9021 | 13de71b4768609f6bb147eb160b27fb0300c132bb42342b1983a64115b47d765 |
| examples/output/data_entry_checklist.json | generated_json | yes | 4810 | ccf2ab74707973f75fca7bfa4893c43efc567b415a0b290410b0e7046cc2bcb6 |
| examples/output/data_entry_checklist.md | generated_markdown | yes | 3728 | e062c650d5b19fec6618040bfe6e5ea6305e2e06935059e480cd45a571db497b |
| examples/output/demo_compare.json | generated_compare | yes | 2302 | 788bb4fbbc3b3f333e9e0811a43fcb5bc7736a181c1c23ddafb2d38a91070cfd |
| examples/output/demo_compare.md | generated_compare | yes | 1630 | e64ec3068e16a27840ca417616ca3801402c00bb2bbbd91011ac6895a2d93951 |
| examples/output/demo_dashboard.html | generated_dashboard | yes | 6551 | 4a1fd4d23e76a78faac2def7b0a5cd98ace64688b235c437f19389fbbc9f0468 |
| examples/output/demo_prior_report.md | generated_markdown | yes | 1486 | 4df746a83c401097b72d82465a8f7f09311d573a00b05753f2ee943a6561e40e |
| examples/output/demo_prior_snapshot.json | generated_json | yes | 3259 | 787e3b70ae49c62d181712bd09bc5fa469a6b89515ed063d57dcd6df8241bf38 |
| examples/output/demo_report.md | generated_report | yes | 1963 | 437e5fea10a983bf2f87c3ce6417a1d70f2f1fa0c9d9f46f452a5e291fcd484d |
| examples/output/demo_review_queue.json | generated_review_queue | yes | 4546 | 7414442d6c628f0df7b96382f539cd1eb41e2742447083c67438630aaa2db99b |
| examples/output/demo_review_queue.md | generated_review_queue | yes | 2517 | 9349b9748ab44084268507a422e1175cd177926466981423cef0b4d785fea2a5 |
| examples/output/demo_review_queue_items.jsonl | generated_review_queue | yes | 41248 | a169937fa0ef622a87a22e9039c1d33440fc2f8001fc14be3332b403926cb30a |
| examples/output/demo_screenshot_guide.json | generated_json | yes | 4455 | 67812bdf6fb3df3bf39df29b2ac2b64ff89c43ccb108c06d8b3f6adaa240a85c |
| examples/output/demo_screenshot_guide.md | generated_markdown | yes | 4015 | 567e6930419020133328f677b92d8a7b7116d4e906b09b36a88dfcd94d256476 |
| examples/output/demo_snapshot.json | generated_json | yes | 6708 | aa6b2e30f3317dbf1b77a2ac5eaed9e220f61341da5492c3b26677331d5d2f2e |
| examples/output/doctor.json | generated_local_only_audit | yes | 1095 | bc81219f20035fd0bacfe4a0a6f4173e5499a513d9bd88b49e7afe4c6603364f |
| examples/output/doctor.md | generated_local_only_audit | yes | 957 | adf003b58e848287df3371066c1a702d2aa737d9026eea5e79191464454ae3b8 |
| examples/output/energy_infrastructure_dashboard.html | generated_dashboard | yes | 8996 | 70ee3a85f729013f1cf0736b9ebbcb4124b8c7b4563a5bf6db0ccfb76b46c291 |
| examples/output/energy_infrastructure_report.md | generated_markdown | yes | 3118 | 7c2c41b383524076b2825d943e87bb80b74e427889e23817ac800d09a316bba6 |
| examples/output/energy_infrastructure_review_queue.json | generated_review_queue | yes | 7925 | 43b81e04f6e7c8442474897d4dd708d0643ec5f3e3e3dc3c4dd233687928a09d |
| examples/output/energy_infrastructure_review_queue.md | generated_review_queue | yes | 3372 | 66d7f429d8d87138382dcf7d635b099f2f1a2c79b2bc50043d7f2518c688a0d5 |
| examples/output/energy_infrastructure_snapshot.json | generated_json | yes | 13247 | 0174c737dab9c71f9efde037b0d7cc0b832e9bb831b9e8f04dab29c115cb30a6 |
| examples/output/examples_index.json | generated_json | yes | 31808 | 4582eeec0e6f1478fc1d5ce9e1d94da0d5291085613f96a2bf9c206dc8f03a19 |
| examples/output/examples_index.md | generated_markdown | yes | 14153 | 7a08ae04c5d98d8059b3158d8eda4a1a38499ab656b28f0082d51ee65d5aaed4 |
| examples/output/fixture_catalog.md | generated_markdown | yes | 5300 | f92441cccdb564f9814114b49582e629357f55fe48d89f49bbcd90f0c82285db |
| examples/output/fresh_clone_plan.json | generated_json | yes | 7642 | 8d196eeb5c65e65c9fb2d985334da2a1093e374386abf0c1d663b0a29131128f |
| examples/output/fresh_clone_plan.md | generated_markdown | yes | 6803 | d83992cf12eb71a2fe1ee704ed34e2bce3f4f6e4a88994eda90c288ef4d67cac |
| examples/output/handoff_packet.json | generated_handoff_packet | yes | 2184 | dd6a7c176ecd07df6083b5d37369080bbdd1b96743770afb779dfb1e7b150947 |
| examples/output/handoff_packet.md | generated_handoff_packet | yes | 1883 | 4bb038fc18a6e3acffe8ac69ce3b887cb46dd5218f193f6b91691d8a6bac8e3a |
| examples/output/handoff_packet_examples.json | generated_handoff_packet | yes | 8052 | 8c011ea02a230a79dfa56e20688df3e3664c0f6bc2d1a31ac9250c7f3bc938fc |
| examples/output/handoff_packet_examples.md | generated_handoff_packet | yes | 3585 | 9c35e024d836f68f976bbaa820017a8729ae63c32465ae73a3a789861379c514 |
| examples/output/integration_notes.json | generated_json | yes | 3681 | c948a610d203f214ae8deff95408925caf0c89f52e08c91fc11c3f41ca79c06d |
| examples/output/package_audit.json | generated_local_only_audit | yes | 10549 | 4cbc495699abe42d5e7746eba1d8db27b4051049fa57b62b06e4dc85bcffed85 |
| examples/output/package_audit.md | generated_local_only_audit | yes | 8457 | 05795adca4bd1d4817eaeb97c0336ae4a50a945c53aa9f4dac7a6ad7d5326ae1 |
| examples/output/playbook_output_examples.json | generated_json | yes | 3945 | f7f7d4c0df3f1223acc109757e28f58d448651bb3fdc4479225c24e0e1857fdc |
| examples/output/playbook_output_examples.md | generated_markdown | yes | 2680 | 4f2177c48f9a066bac064e9ba5027de83e333ee1c2acd3306d066ddfa48ec706 |
| examples/output/playbooks.json | generated_json | yes | 4439 | ddbe6e7b30eacf6cececb7d51aada4994484ab89015ca204442c9dfeb252118a |
| examples/output/playbooks.md | generated_markdown | yes | 4252 | 7c7b23e5fdc2033e5d6ea6f918daeba550ecc129955f3ec7fecb4582dfed1966 |
| examples/output/promotion_pack.json | generated_json | yes | 3855 | 37fb89424d769ea0c202c307ff70b6d5aa7f5ed7d5639ef9ebabc68930a70bb1 |
| examples/output/promotion_pack.md | generated_markdown | yes | 3005 | 78175e92c31872d1b8a65f7cab12a2875ab1874dae57305764c1a5bc0b1bd174 |
| examples/output/public_apple_static_case_study_dashboard.html | generated_dashboard | yes | 8740 | 2903f6bea935c18763d6c63871585133108615aa6d68252199019167df06a7b0 |
| examples/output/public_apple_static_case_study_report.md | generated_markdown | yes | 4000 | 21d8f9adf6f7cd37b9b3787d23eed2e3759627e08905c59471bb53c6d1b6d53b |
| examples/output/public_apple_static_case_study_review_queue.json | generated_review_queue | yes | 6322 | 145c1b17421fbdaf87ab469c0964aec888378cc01ef323735436045b8fc7ccd6 |
| examples/output/public_apple_static_case_study_review_queue.md | generated_review_queue | yes | 3772 | b78fca3c30ae917fbb274a765c81bf0c32b92f37156aa9db80fefff6b496e4db |
| examples/output/public_apple_static_case_study_snapshot.json | generated_json | yes | 10198 | 19b5dbffafcd895df35ce12f3b36850af3e1ad6cfab6d82df1f8df4271e17318 |
| examples/output/publication_checklist.json | generated_json | yes | 5510 | cfc53d1078772496f5f6d61dc10a1202668f4e59b806f9f9eb4bc1c7f697d21f |
| examples/output/publication_checklist.md | generated_markdown | yes | 4265 | b44c2e2db209657a5aec13ef26a64420de59426d9945c3d2a0def66e0b9ade01 |
| examples/output/risk_language_taxonomy.md | generated_markdown | yes | 3580 | cc096790eadb320013fc5c6667a928b996678e8e855035937dc4c232ee364fbc |
| examples/output/sample_filled_template_report.md | generated_markdown | yes | 4458 | 75cf8616b6848b73d4d87541f0b4a36814f6758d6d774170d1ecee80aa6f733f |
| examples/output/sample_filled_template_review_queue.json | generated_review_queue | yes | 6477 | 150baef6a3eb73b5830e0967750421c61ecd0eaa7911d779f9085f4dfb43e3b6 |
| examples/output/sample_filled_template_review_queue.md | generated_review_queue | yes | 3583 | f193f16e904985065dc8aba089e425103a058e9207e01d88069aa493514ac924 |
| examples/output/sample_filled_template_snapshot.json | generated_json | yes | 11793 | 5dec987e752a8f6b7b3895c178f352ae2023f895a5a38794b2cbe0960522c3d6 |
| examples/output/schema_authoring_reference.json | generated_json | yes | 9671 | e33aa48003be6b88e6cc8cf7bba1a33523c5cc02bd520ec1a10f51907ec32aff |
| examples/output/schema_authoring_reference.md | generated_markdown | yes | 7328 | cb0e6e755a831365e504d85a0493a96a3022d3874584815a785ed1857a73b47f |
| examples/output/semiconductor_equipment_dashboard.html | generated_dashboard | yes | 10623 | 6dd5034d6ad1b1adb792bfc46ac629e21ad0616e85587ea18784ef6f589529f0 |
| examples/output/semiconductor_equipment_report.md | generated_markdown | yes | 5369 | 8f17216a89545bbf2b30fb747acb092e947a7e9b3d82ba0ca646db99ac497402 |
| examples/output/semiconductor_equipment_review_queue.json | generated_review_queue | yes | 8353 | 28a7e2ea34370a53dc937a1a0fc423032eedf1d75a1d2b13fbca08e2c44be1dc |
| examples/output/semiconductor_equipment_review_queue.md | generated_review_queue | yes | 4647 | edd1c5dce147befe6204c30484f40b0915775ed599b2c09c32d4172ccb59774a |
| examples/output/semiconductor_equipment_snapshot.json | generated_json | yes | 13364 | 29753cda7a59306689f937de1b8feeeb41ce82a0165d93c4cbe4553b3f4cce44 |
| examples/output/showcase_dashboard_preview.svg | generated_dashboard | yes | 4556 | e7e8ae708650d6c704ff46526131fa922ae3116380bb8011bca6633879e61ff0 |
| examples/output/source_boundary_evidence.json | generated_json | yes | 17242 | ff286be435f12df48b74201ae02780159b1c51f877779b8b95c42bff27427505 |
| examples/output/source_boundary_evidence.md | generated_source_boundary_evidence | yes | 7738 | 345226d8f66692565991250fea820fbf5e9ed8ee3082d00ba82e8267486cf32c |
| examples/output/template_catalog.json | generated_json | yes | 6130 | 871b99977b69f7db27ac3b1987faa7177345d4549075178f8fcc707dfd1f1d6e |
| examples/output/template_catalog.md | generated_markdown | yes | 4758 | 4b79e8cbf2ee19385858ec77826befd45357e034e9ae3e2b7505530b2171f39a |
| examples/output/visual_evidence_receipt.json | generated_json | yes | 9159 | 9cabb15dce945da76b696726540ade7d8c255ae249e71dbb95ed817440a4211a |
| examples/output/visual_evidence_receipt.md | generated_visual_evidence | yes | 5308 | eb31e2248412eb5497b6f8698467f9f0d6fc4a1df2f489cbbb7c9d84ce8db68d |
| reports/maturity/maturity_evidence.md | release_evidence | yes | 15338 | a8c558d5281e6bd57701d306cc2e4fbc076173a3223a638cd2a75386f76f76ab |

## Source Notes

- Audit uses local repository files only and records metadata, not artifact contents.
- Source fixtures are user-authored or static public-source examples; reviewers must verify source URLs and filings/transcripts before relying on them.
- Generated reports preserve source-boundary labels for management claims, analyst questions, and user synthesis.

## Freshness Notes

- The audit does not fetch live market data, current filings, current transcripts, quotes, prices, or broker data.
- Freshness readiness depends on each fixture's as_of, data_cutoff, item dates, stale badges, and reviewer source checks.
- Regenerate demo artifacts after changing fixtures, scoring, rendering, docs, or release evidence.

## Review Readiness Notes

- Ready means handoff artifacts are present and hashable; it does not mean source evidence has been independently verified.
- Reviewers should inspect missing-evidence and stale-data queues before using reports in any downstream research workflow.
- Use the generated handoff packet and source-boundary evidence together so downstream owners see cautions and provenance.

## Missing Evidence Items

- None

## Recommended Evidence Items

- Confirm source URLs, source names, publishers, and accessed_at dates before public handoff.
- Confirm stale/static badges are acceptable or regenerate fixtures from current source documents.
- Keep screenshot or visual evidence receipts paired with static HTML dashboards.
- Keep review queue and handoff packet artifacts beside the main Markdown report.

## Regeneration Commands

- `PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output`
- `PYTHONPATH=src python -m earnings_call_risk_map evidence-handoff-audit --root . --format markdown --output examples/output/evidence_handoff_audit.md`
- `PYTHONPATH=src python -m earnings_call_risk_map evidence-handoff-audit --root . --format json --output examples/output/evidence_handoff_audit.json`
- `PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity`
