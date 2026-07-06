# Evidence Handoff Audit

- Schema: `earnings-call-risk-map.evidence-handoff-audit.v1`
- Package: `earnings-call-risk-map`
- Version: `0.9.7`
- Root: `<redacted-root>`
- Checked artifacts: 99
- Present artifacts: 99
- Missing artifacts: 0
- Source fixtures: 7
- Generated outputs: 84
- Readiness: `ready_with_review`

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Boundaries

- local/static fixtures only
- no live data
- no broker connection
- no personalized investment advice
- no legal advice
- no accounting advice
- no tax advice
- no buy advice
- no sell advice
- no hold advice
- no private data

## Checked Artifacts

| Relative path | Role | Present | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| README.md | documentation | yes | 22452 | 1ab616724a3bd468b21f00c4c13d7ff39bba37a885a7bfdde7bfe9ae32efa9f6 |
| docs/case-study-limitations.md | freshness_documentation | yes | 4394 | 0a32fc024096b127572c02b86b4ac2529a089aa9e42bffc273bf9707f0f910dd |
| docs/non-advice-boundary.md | source_boundary_documentation | yes | 3689 | 8bd98218315757cd15e9edfe0e59f0f315dc1ac0c5dc96e438312a89ea09fb42 |
| docs/reviewer-evidence.md | reviewer_handoff_documentation | yes | 7578 | 00dc158405f39f87c717d49ed006d7a191b94c8a4ef59bc8b87abf05889a3eba |
| docs/security-and-privacy.md | source_boundary_documentation | yes | 3220 | b6829083ba45a2af5ee38e850aefa395c73dbef50e689334dae23613acff3b14 |
| docs/source-attribution-guide.md | source_boundary_documentation | yes | 6714 | 1db47eb6bde1e8264ede9ca93379d136a32e7300d06b9b42dbe513ad54370890 |
| docs/usage.md | documentation | yes | 26421 | a1d0a7cf63d2ff83bf82a8b88171f531ea301042f2732c8265732bae99f19160 |
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
| examples/output/command_cheat_sheet.json | generated_json | yes | 4451 | 18e0fb0c0775699718ae3ad7b9e885b0ad960771bee57a4db723c60d496124f1 |
| examples/output/command_cheat_sheet.md | generated_markdown | yes | 2882 | 198309f450e70316c26cc643f8cd52c3a82b3d851511138c3c779fdd5856b0fe |
| examples/output/command_cheatsheet.json | generated_json | yes | 4451 | 18e0fb0c0775699718ae3ad7b9e885b0ad960771bee57a4db723c60d496124f1 |
| examples/output/command_cheatsheet.md | generated_markdown | yes | 2882 | 198309f450e70316c26cc643f8cd52c3a82b3d851511138c3c779fdd5856b0fe |
| examples/output/consumer_hardware_dashboard.html | generated_dashboard | yes | 9023 | d67292c12a2a4a5fb6c990887161d14d98cf5087a0f3710e6bb95b55233c2ceb |
| examples/output/consumer_hardware_report.md | generated_markdown | yes | 4362 | 3ff837101da52f6fa90ec9753631c3ebdb86ac945b7be342cb5678b2f1f6cf39 |
| examples/output/consumer_hardware_review_queue.json | generated_review_queue | yes | 4338 | 698171da5f79d30629a779438d730b2af1b630fe2443930ce1b59f2b64641b09 |
| examples/output/consumer_hardware_review_queue.md | generated_review_queue | yes | 3143 | c22c2b4243927fff10f03ca8187590a1ad69b6c2d766ad5bcfd125ad4ea80ae3 |
| examples/output/consumer_hardware_snapshot.json | generated_json | yes | 9021 | ddc5b10865121c34efd9347491631d5e6734b642564d4b312251df0cd15240e5 |
| examples/output/data_entry_checklist.json | generated_json | yes | 4810 | ccf2ab74707973f75fca7bfa4893c43efc567b415a0b290410b0e7046cc2bcb6 |
| examples/output/data_entry_checklist.md | generated_markdown | yes | 3728 | e062c650d5b19fec6618040bfe6e5ea6305e2e06935059e480cd45a571db497b |
| examples/output/demo_compare.json | generated_compare | yes | 2302 | eaf58c843a7a24ca3e48825dffbc026c69dce5f14ec6b0cb931a6aaf9dba2a5a |
| examples/output/demo_compare.md | generated_compare | yes | 1630 | e64ec3068e16a27840ca417616ca3801402c00bb2bbbd91011ac6895a2d93951 |
| examples/output/demo_dashboard.html | generated_dashboard | yes | 6551 | dbcc5d0a0b761b2affb0cc295d29a54edeec22b9cd8534c839d2e1641b14d6b7 |
| examples/output/demo_prior_report.md | generated_markdown | yes | 1486 | 3085399f0edb6808152308e5560d70f79fbee06f429ff72a50d61c72741150f9 |
| examples/output/demo_prior_snapshot.json | generated_json | yes | 3259 | d47a7191d0215ed81c3cf900929bc2ce8e957763e11eb7f0a6408a01bac7ecd6 |
| examples/output/demo_report.md | generated_report | yes | 1963 | 0654432795d6ad181cbe0416fa697015138dd5868fbb42bc699424c8a77f9047 |
| examples/output/demo_review_queue.json | generated_review_queue | yes | 4546 | 2774b9ddc91b92869136a7f63f44888f6b9b80198d7c7b82ac6c7ce2fcc2a2af |
| examples/output/demo_review_queue.md | generated_review_queue | yes | 2517 | 000a1ef1363286b2f5670da02436815f01100209598db5b50e53b72715bb7bb3 |
| examples/output/demo_review_queue_items.jsonl | generated_review_queue | yes | 41248 | a169937fa0ef622a87a22e9039c1d33440fc2f8001fc14be3332b403926cb30a |
| examples/output/demo_screenshot_guide.json | generated_json | yes | 4455 | 67812bdf6fb3df3bf39df29b2ac2b64ff89c43ccb108c06d8b3f6adaa240a85c |
| examples/output/demo_screenshot_guide.md | generated_markdown | yes | 4015 | 567e6930419020133328f677b92d8a7b7116d4e906b09b36a88dfcd94d256476 |
| examples/output/demo_snapshot.json | generated_json | yes | 6708 | 733b8f8919c8c324a5f78ddd4b922445d977d172b1b8eb37af12524b79d44ec2 |
| examples/output/doctor.json | generated_local_only_audit | yes | 1095 | e8ec74b4281be02010a91cb06692a1b80653a3ef0df43798bea647440e23f790 |
| examples/output/doctor.md | generated_local_only_audit | yes | 957 | 5d82dd3bb5dd3ef41b160ad89a327c9230706d1650019c52b1a798a43d2672ab |
| examples/output/energy_infrastructure_dashboard.html | generated_dashboard | yes | 8996 | 767bb99b2242db2673c1ae04e72b21fdbccf1b34b1bf9172b71408a1f63d7977 |
| examples/output/energy_infrastructure_report.md | generated_markdown | yes | 3118 | 3ed6f8368b0b5d04f5e252714f12cad0012e6819732beacb0d211a25daf38a67 |
| examples/output/energy_infrastructure_review_queue.json | generated_review_queue | yes | 7925 | fec165190819b40ee5f52b4e6ff2f283bd7f048aff42f37928f78b7b7a8609b5 |
| examples/output/energy_infrastructure_review_queue.md | generated_review_queue | yes | 3372 | a8c5d22ab822ac65d19ab933b21609a3d61e1fc9461e088e9e11743fe810f4e7 |
| examples/output/energy_infrastructure_snapshot.json | generated_json | yes | 13247 | 0e592da2cdea1b456308b326b4fb8271da8aebf6464d4e2c3bd5fad425e6fae8 |
| examples/output/evidence_handoff_compare.json | generated_compare | yes | 3501 | e5a7581d05de809b22364cb75ed1c6198d4d955978bfb76552a293db0de0ec27 |
| examples/output/evidence_handoff_compare.md | generated_compare | yes | 1980 | 7d222c9926474c13d91b86f337c16fa519d8878e3e2c7883c9877ab5a9e1e069 |
| examples/output/evidence_handoff_compare_demo_after.json | generated_compare | yes | 1634 | 92c72e068e0087e667c9fdc054c54bb377bf87c56a98a7680945d805f4cd364e |
| examples/output/evidence_handoff_compare_demo_before.json | generated_compare | yes | 1437 | a22956b1f332aef13d23559faec66009d01b67aa7621aedc207c131c75ca4bff |
| examples/output/examples_index.json | generated_json | yes | 33239 | 4630816c8088eb6f8060e533fb1574ca3e2182f7e062c110ec22729c768c9a97 |
| examples/output/examples_index.md | generated_markdown | yes | 15008 | 30f1c79dcbcd65535543f6c75981a5978dbf073e59e0b5140a7823429b2e7e6a |
| examples/output/fixture_catalog.md | generated_markdown | yes | 5300 | f92441cccdb564f9814114b49582e629357f55fe48d89f49bbcd90f0c82285db |
| examples/output/fresh_clone_plan.json | generated_json | yes | 7642 | 24811d15e01e29a1c38b2426f37ac0584493365c2385e9e46d43ba8ee71ea3d6 |
| examples/output/fresh_clone_plan.md | generated_markdown | yes | 6803 | 17fd30e7b87f783b32cbe5820a55c5157ec0278f452c3f1b465bf31cb30c0cef |
| examples/output/handoff_packet.json | generated_handoff_packet | yes | 2184 | 92c24379b1777ea832abb33bfbea65daa99eddb955aeb1891ed9187bafae2360 |
| examples/output/handoff_packet.md | generated_handoff_packet | yes | 1883 | 159f38c1d6093d6980bb2defb4f9346f4161b0e1a956da78dbd0825de9ea46ec |
| examples/output/handoff_packet_examples.json | generated_handoff_packet | yes | 8052 | 7f7bccfe05ea22ebe526ce8bc07b90b676cd985e1a3c4ce2eccc6c3d2413f5d4 |
| examples/output/handoff_packet_examples.md | generated_handoff_packet | yes | 3585 | 9c35e024d836f68f976bbaa820017a8729ae63c32465ae73a3a789861379c514 |
| examples/output/integration_notes.json | generated_json | yes | 3681 | c948a610d203f214ae8deff95408925caf0c89f52e08c91fc11c3f41ca79c06d |
| examples/output/package_audit.json | generated_local_only_audit | yes | 11242 | 87b80107c1bfd2ce3492c2736e9934b5fb28c33889250dc8ad36d2953c9725cf |
| examples/output/package_audit.md | generated_local_only_audit | yes | 9026 | 3420423d8400fd1bb54b9369937dcdaba3565658fda9e3a4f3a78aa70e83e878 |
| examples/output/playbook_output_examples.json | generated_json | yes | 3945 | f7f7d4c0df3f1223acc109757e28f58d448651bb3fdc4479225c24e0e1857fdc |
| examples/output/playbook_output_examples.md | generated_markdown | yes | 2680 | 4f2177c48f9a066bac064e9ba5027de83e333ee1c2acd3306d066ddfa48ec706 |
| examples/output/playbooks.json | generated_json | yes | 4439 | ddbe6e7b30eacf6cececb7d51aada4994484ab89015ca204442c9dfeb252118a |
| examples/output/playbooks.md | generated_markdown | yes | 4252 | 7c7b23e5fdc2033e5d6ea6f918daeba550ecc129955f3ec7fecb4582dfed1966 |
| examples/output/promotion_pack.json | generated_json | yes | 3855 | 1f418741e91a6b9bf57fdf94df2c452cffb4c846cd8260d43b9197c45f0b1d2b |
| examples/output/promotion_pack.md | generated_markdown | yes | 3005 | 8061dec8e1e5c7609dfa955440694f988e1ecc124601e730904cdc84fc2708ed |
| examples/output/public_apple_static_case_study_dashboard.html | generated_dashboard | yes | 8740 | ed741976f2a7a8068b3b0b753497ccad87488a5084293983e9534b321e85f006 |
| examples/output/public_apple_static_case_study_report.md | generated_markdown | yes | 4000 | 78ace564b0d0280f32a9788d23ea9d14c2458d2e00237343eb5b86cc79de6746 |
| examples/output/public_apple_static_case_study_review_queue.json | generated_review_queue | yes | 6322 | c4e3cd7653234486223b61cd20ebdc01ba1c3567f25139fc444933626a7b45b4 |
| examples/output/public_apple_static_case_study_review_queue.md | generated_review_queue | yes | 3772 | 6557f67fe3d590fbc841093089c0b6b2b05064bd75f19c673fb3454caae6b201 |
| examples/output/public_apple_static_case_study_snapshot.json | generated_json | yes | 10198 | 3d25bedd9972f05b6b4dc106c3f7660b5f8521a4d0f03686c003c398b590d586 |
| examples/output/publication_checklist.json | generated_json | yes | 5510 | 3c2fc032bfb4d93f8b263b102de662ed457381f9bddf9a57d828a0569c64fa3a |
| examples/output/publication_checklist.md | generated_markdown | yes | 4265 | 6141ffa3d67900ae847d5a749cfd10866c3aeaa58c121ae9bbc76a701d61f26a |
| examples/output/release_owner_compare_blockers.json | generated_compare | yes | 6186 | b3f21cfd057daf41d320b232e3158e7da74370c3d671a9c3fa775a7f8fc33ad2 |
| examples/output/release_owner_compare_blockers.md | generated_compare | yes | 3342 | abea7ab58f2be83b29d2ff4b54c89da10fbac5e4b45e7743f7d3651b8d5f3181 |
| examples/output/risk_language_taxonomy.md | generated_markdown | yes | 3580 | cc096790eadb320013fc5c6667a928b996678e8e855035937dc4c232ee364fbc |
| examples/output/sample_filled_template_report.md | generated_markdown | yes | 4458 | 75cf8616b6848b73d4d87541f0b4a36814f6758d6d774170d1ecee80aa6f733f |
| examples/output/sample_filled_template_review_queue.json | generated_review_queue | yes | 6477 | 150baef6a3eb73b5830e0967750421c61ecd0eaa7911d779f9085f4dfb43e3b6 |
| examples/output/sample_filled_template_review_queue.md | generated_review_queue | yes | 3583 | f193f16e904985065dc8aba089e425103a058e9207e01d88069aa493514ac924 |
| examples/output/sample_filled_template_snapshot.json | generated_json | yes | 11793 | 5dec987e752a8f6b7b3895c178f352ae2023f895a5a38794b2cbe0960522c3d6 |
| examples/output/schema_authoring_reference.json | generated_json | yes | 9671 | e33aa48003be6b88e6cc8cf7bba1a33523c5cc02bd520ec1a10f51907ec32aff |
| examples/output/schema_authoring_reference.md | generated_markdown | yes | 7328 | cb0e6e755a831365e504d85a0493a96a3022d3874584815a785ed1857a73b47f |
| examples/output/semiconductor_equipment_dashboard.html | generated_dashboard | yes | 10623 | 96e1c34010195731ce3bedb531596774af629c55d612f4cf3de34f869ed84634 |
| examples/output/semiconductor_equipment_report.md | generated_markdown | yes | 5369 | 0a6e6ad8d4a088d70403bffbef9319000433b9daf4e8dd04f039ac6a420cef20 |
| examples/output/semiconductor_equipment_review_queue.json | generated_review_queue | yes | 8353 | f2aac951f61667985c86670c909862f5021784cedf8507766fdade9c1bc16e98 |
| examples/output/semiconductor_equipment_review_queue.md | generated_review_queue | yes | 4647 | 577e2d7ed2b8e00d0fa6976c2d0f7e9f673fb33dd85e8a83098bf89b807b0975 |
| examples/output/semiconductor_equipment_snapshot.json | generated_json | yes | 13364 | 79d16d304c5e879f7e418bdd4fe00984ea8783d5c6699879b1c2d868828c63e1 |
| examples/output/showcase_dashboard_preview.svg | generated_dashboard | yes | 4556 | e7e8ae708650d6c704ff46526131fa922ae3116380bb8011bca6633879e61ff0 |
| examples/output/source_boundary_evidence.json | generated_json | yes | 17242 | ee7be32891be6b2e9090ce0ca031e8be3d3ee91d12bda31c6aec77229c090a7d |
| examples/output/source_boundary_evidence.md | generated_source_boundary_evidence | yes | 7738 | e10179e5b015fb7843ba02cb14eb0201dcf15f065eb4907bdd2de7fd36d5b45e |
| examples/output/template_catalog.json | generated_json | yes | 6130 | 871b99977b69f7db27ac3b1987faa7177345d4549075178f8fcc707dfd1f1d6e |
| examples/output/template_catalog.md | generated_markdown | yes | 4758 | 4b79e8cbf2ee19385858ec77826befd45357e034e9ae3e2b7505530b2171f39a |
| examples/output/visual_evidence_receipt.json | generated_json | yes | 9159 | a83d05fe1d64d80264eaa87c67be6e31f3cc156597b750395a49c34f781326ef |
| examples/output/visual_evidence_receipt.md | generated_visual_evidence | yes | 5308 | 7ef68aec5d7e1d515cdc349b5ee5dfc9a26f6bd6829f79f64d18a08d4dcdd3a1 |
| reports/maturity/maturity_evidence.md | release_evidence | yes | 17056 | 002b58cccb06e33e260b5d73d7b06256ce518201ec5ab3738f0721e1e05604af |

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
