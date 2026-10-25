# The raw session files

_Generated 2026-10-25 17:04._

The transcripts in [`logs/`](logs/) are **exports**. They were produced from the files listed below by [`tools/`](tools/), and that is the one fair objection to them: you have to trust the exporter. This page is the answer that does not require trusting anything.

**132 raw files, 848 MB, 69,450 JSON records.** Each row fixes a file by its SHA-256. Anyone given the archive can confirm the files are the same ones, unaltered, and re-derive the published transcripts from them.

**Root hash over the whole set:**

```
792261eb5a265ad9e3066010064699a20efa6f10aa395b8d1bb35b8b298c8abc
```

That value is computed over every per-file hash below, in sorted order. It sits in a commit whose own hash is anchored to the Bitcoin blockchain by the proofs in [`timestamps/`](timestamps/), so the set cannot be substituted after the fact without the anchor failing.

## Why these are not published

Three reasons, and the first is the one that decides it.

**They carry the book in bulk.** About a quarter of their bytes is tool traffic — whole files read into context, which for this project means chapters. The exports collapse every tool result to a marker, which is why 896 MB of raw becomes 6.6 million words of readable conversation. Redacting prose out of escaped JSON string fields is a different and far riskier job than redacting paragraphs, and a mistake in it would not be visible.

**Size, and one file settles it.** The set is 896 MB: 384 MB of uncompressed `.jsonl` plus three compressed archives of the longest sessions that come to 510 MB between them. One of those, a single Codex session, is **354 MB** - three and a half times GitHub's 100 MB hard limit, so it could not be pushed at all. And everyone who cloned the repository would pull the lot to read one day of work.

**One credential was pasted into a session by mistake** and blanked from the saved exports. Whether that blanking reached the raw files has not been established, and bulk-publishing them before it was would be careless.

They are held in the private archive and shown in full to anyone who asks and has a reason: an agent, a publisher's lawyer, a registration examiner, a journalist.

**Two or more files below share a hash.** That is not an error: the same session was exported twice under different names, so the files are byte identical. Listed rather than deduplicated, because the manifest records what is in the archive.

- `30a19baa323a1535` : `2026-09-23_0c7d31e3.raw.jsonl`, `2026-09-23_0c7d31e3.raw.jsonl`

The published transcripts in `logs/` are named `date_sessionid`. The raw files
below carry the working directory as well, which is how the tools name them; the session
id is in both, so the two can be mapped to each other.

Three published names end `_2` or `_3`. Two session ids were exported from more than one working directory, one of them from three; the published name drops the working directory, so those exports would otherwise collide on a single name. The largest keeps the plain name and the others are numbered by size.

## How to check a file you have been given

```
sha256sum <file>          # Linux, macOS
certutil -hashfile <file> SHA256   # Windows
```

Compare the result with the row below. A match means it is the file this archive recorded on the date above, to the byte.

## Claude Code

_70 files, 372.8 MB, 61,087 records._

| File | Bytes | Records | SHA-256 |
|---|---|---|---|
| `2026-09-18_087c1f14.raw.jsonl` | 5,526,037 | 859 | `92fcf693729197c341994dcb4838ee6093b1c37249ca277fc883b4e440d55843` |
| `2026-09-19_35f385b5.raw.jsonl` | 5,452,985 | 1,153 | `9cd06ccd28040de45c40af9e7b768ed335a86189899f72f6dc5f2d598cf0f0a7` |
| `2026-09-19_ba41bc4b.raw.jsonl` | 13,909,213 | 4,177 | `753f1f46c73061229b7098ef6e940dbdef16290ef95fe550575ecd9769524909` |
| `2026-09-19_c720c8bc.raw.jsonl` | 2,181,354 | 523 | `d0d966b1c5d09ffbd0548d8e1147df88997d3bee0d864f79b98e889d1f762c8e` |
| `2026-09-21_014bace2.raw.jsonl` | 35,724,140 | 14,329 | `d33c0e86f303d35f4b2ddfabe2597b2cf6e7c7d4b4460e53f92bd1275ace3629` |
| `2026-09-21_07b84eab.raw.jsonl` | 580,479 | 128 | `f7fd9a8875bea016a489e9fa8422a5703163d98d2c0c87a391c302a6d490a873` |
| `2026-09-21_15164568.raw.jsonl` | 3,897,664 | 901 | `a8887f6261e59cfcc2c8bfdcfa91b6ef0cef8404b8e5a43928dfe1003c5cb0e6` |
| `2026-09-21_41880b84.raw.jsonl` | 3,794,589 | 791 | `bd93118c4bb189144aedd08cc189171df9768ef641af65979f4b4187eb3b096a` |
| `2026-09-21_4e6a64e2.raw.jsonl` | 2,089,061 | 823 | `815363b5a87967cd40e22d93287d3fca66f6be166bd9380fbbc2b0335b2cbbbb` |
| `2026-09-21_53901afb.raw.jsonl` | 616,683 | 129 | `f93e99521662976673d0695d698aac0f779d1c6a606e2a3b7ceaecce28a82659` |
| `2026-09-21_61ed6bc5.raw.jsonl` | 3,616,970 | 1,095 | `4450b7f194ae38caf988bb32be2e87bd53db55c68168d0da19481046ca72ef62` |
| `2026-09-21_91a0d312.raw.jsonl` | 731,672 | 194 | `86f6ba8f63a83089969045b10d4121428db84ecd3976509ec69636043d55060c` |
| `2026-09-21_96c31bbb.raw.jsonl` | 4,515,925 | 1,233 | `d593ba0b686aae97b7420d040114e26e294e8a1c1dc8847a62c721832b8757ae` |
| `2026-09-21_9ee17a7b.raw.jsonl` | 390,960 | 71 | `fd80787101969c2cdd0dc57bb0f9e50e9ed62395f5d9da77f12011b055939959` |
| `2026-09-21_c36622df.raw.jsonl` | 523,362 | 128 | `76b368d54e3dada31c832a11d0cf63798f134cd6950f0a33adf46bba31703049` |
| `2026-09-21_e04dbcb6.raw.jsonl` | 901,922 | 277 | `a7578e18e21db93dac3e029ba27f21315c9a2065f739225c8217bea5ff67f2b6` |
| `2026-09-22_323b0cdf.raw.jsonl.gz` | 37,689,763 | compressed | `59d42091e10a3ffdda45ee152e2ba01d590cbf0d46485c2f46c3684d033674ef` |
| `2026-09-23_0c7d31e3.raw.jsonl` | 16,842 | 9 | `30a19baa323a15350869cbc1ad6d886df2719d93339f0469ae5bea54f49dc225` |
| `2026-09-23_0c7d31e3.raw.jsonl` | 16,842 | 9 | `30a19baa323a15350869cbc1ad6d886df2719d93339f0469ae5bea54f49dc225` |
| `2026-09-23_7ce9d96e.raw.jsonl` | 721,155 | 131 | `0bb5180ecea158436c9d968eb6108ab86ee36ff7a4c32fb3063f46e6461af119` |
| `2026-09-23_b2a6e6ab.raw.jsonl` | 17,176 | 10 | `33a3644e05ae54e8efb30a73f8ccd8e826cfd140ec7c7143eb1743a148dfc721` |
| `2026-09-23_e2fdf8f3.raw.jsonl` | 20,659 | 10 | `c43852a584cf306674567b1649a877fdae60388ed9815bbf359bd677e97db33d` |
| `2026-09-24_347168f9.raw.jsonl` | 284,156 | 31 | `053359c4f369a5f961b256ec77dff138966c1d721968396eaffe04b803516fc7` |
| `2026-09-25_efc1cf7f.raw.jsonl` | 355,678 | 51 | `00add491178c90d4e7d09174256487973cb50dc37d575d89cf864554b1d5d57d` |
| `2026-09-28_289318e5.raw.jsonl` | 518,996 | 91 | `a99eefdb13dee17622dcf7eacc32b728923e95238d4b3351e22949ae6c4e2965` |
| `2026-09-28_304c43ad.raw.jsonl` | 532,481 | 94 | `d783133924075ba55dd91f418cbcd64f9eb0f07938a06e64dd0cca968edf4be8` |
| `2026-09-28_49e959fa.raw.jsonl.gz` | 62,739,128 | compressed | `cacc589dea0bf06842b82dcd373ea50f35e0971172bae5294fb09b09770fc689` |
| `2026-09-28_abfdacb0.raw.jsonl` | 533,643 | 60 | `36611ac5573f540ffcb671de172f482f10256efce1fdccc28855b3842f949306` |
| `2026-09-28_d85721bb.raw.jsonl` | 30,484,877 | 11,939 | `cceff6496a2c4affb08092c0e6581f46c96739d0de1d876993471bf17b86b44f` |
| `2026-09-28_d85721bb.raw.jsonl` | 32,777,906 | 13,062 | `2b84af80a9a8f38edfc7e2a78634778a5cb22402e44980dd4ce2ac53f87372f5` |
| `2026-09-28_d85721bb.raw.jsonl.gz` | 100,813,156 | compressed | `db48f04768a01ba98a2e2125156b2eac3f543418164bb6cafb5c0a7a9c53dbc0` |
| `2026-09-28_edda1b79.raw.jsonl` | 6,372,839 | 2,751 | `4582212266dd7747d54bd5eba11a97740cd6c06eed4d44ce4aab7694aaa67217` |
| `2026-09-29_deb2940f.raw.jsonl` | 431,345 | 57 | `921a509fc95dd34a2bb6b3f61698efe516b26c9d61de9655a5659094c42e3c2b` |
| `2026-09-30_90a12d96.raw.jsonl` | 421,630 | 45 | `39a12d56fc4498ffb86608745f3bb21ea4021d49c421b6fa85c350dbb44a4d6e` |
| `2026-09-30_94919722.raw.jsonl` | 342,706 | 46 | `2e6092113bc2d1468f122565f5bb258f770f6181a7031662fae342c1dd563a4e` |
| `2026-09-30_c516be1e.raw.jsonl` | 412,937 | 48 | `bdd9d8adf6f58ddfe82d9dd6e7c0802b84371ca1c0cb276aaa05e33fe40bff7c` |
| `2026-09-30_da343b28.raw.jsonl` | 330,764 | 54 | `131d9c1bbdd4f62e2d255021d4381b7cfb633a8f5f94f3ef6fdbdea46f9c2a1f` |
| `2026-09-30_eaf36d41.raw.jsonl` | 316,606 | 41 | `e406634a0794bfc3ebec79be330202e14bada7786729be882bcf93db080c393b` |
| `2026-10-01_66de9103.raw.jsonl` | 482,360 | 54 | `985c04e72833533a7972a91e0e6da5b20e3edafbf74d5806798695e75ba3f6a9` |
| `2026-10-02_80ea9977.raw.jsonl` | 389,876 | 57 | `c7e76d1cf26fa796e91e6fcad6b045162a83452685645597d3688609ee24cee3` |
| `2026-10-03_6a3d8347.raw.jsonl` | 405,020 | 45 | `4822a27e2c2b522dbadc4dae14874cd99eef3fe139ff1f91dbcdb6ad0836f107` |
| `2026-10-05_6e03f6f1.raw.jsonl` | 368,270 | 51 | `b27fbcf2509119b18beb3bdb0bccf5ebcb6cdd28a8cd0b90c5800dfa9c5b575a` |
| `2026-10-05_be71975c.raw.jsonl` | 291,442 | 37 | `29736e6508add301e20c871612939b9a343579043f32a8c87be39317914931be` |
| `2026-10-06_2d32ab99.raw.jsonl` | 871,228 | 127 | `43bcbd81d323f24e0305515ceda675f245c0d5219b0dff4f51de78fc09f490cc` |
| `2026-10-07_127af21e.raw.jsonl` | 395,769 | 50 | `f92fced9fcb9410adc2bb9b917cab957b07cf1d82e60c6f74dd274768a02a9fc` |
| `2026-10-08_bd7038b9.raw.jsonl` | 430,743 | 51 | `850d3ef51fc3318c2cf54cbdb88194d41b7746d121867dff5461402ec7a95f42` |
| `2026-10-09_4a054657.raw.jsonl` | 3,237,591 | 654 | `a2b862246f09cccce1e5be1ea2d0d8f39d0de6e2c443a4f3c4c6ffe9e30a6e31` |
| `2026-10-09_907dc5de.raw.jsonl` | 587,112 | 78 | `0ae65b15e8b2f8930528b729f57849169d05c40c70ba10d7e1a9c7a8dccb2e30` |
| `2026-10-09_973c7889.raw.jsonl` | 466,259 | 64 | `3434d6b06803172d5c54d040c29408c3c1ecb45dbe94f7040f636b030281f61f` |
| `2026-10-10_aaa07372.raw.jsonl` | 546,504 | 61 | `71045cda1e4d54701d2a000422e374ccbdd0e5969ad4809e0835a690cc163206` |
| `2026-10-11_aa36bd21.raw.jsonl` | 519,197 | 68 | `1cf35d1343811da8a08a8e2aeafe513a53a0fbd74a468ffd482b630a21db9e31` |
| `2026-10-12_1c956270.raw.jsonl` | 279,658 | 49 | `25bc2d9d90419085d4260da481885310722c3a15a2c947a6d09b4cf6e75d62f7` |
| `2026-10-13_9045d01c.raw.jsonl` | 930,883 | 160 | `f897b06502ad415d8c8d06aca9b8bd7fd07425bf316efaa17b0d5eed02f24efd` |
| `2026-10-14_afe72d4f.raw.jsonl` | 933,549 | 113 | `d6384698218278a0ecdbad966a553664042c2c26de37ee878f668a5911c12680` |
| `2026-10-15_4b6e6e18.raw.jsonl` | 602,058 | 57 | `13d306edc1d85ce0814fcf393ff995449cc2c704fb7dd37657fe7da922526a32` |
| `2026-10-16_aba11ee0.raw.jsonl` | 1,205,514 | 221 | `d07b212388a1da986a1c804e58b2da6ffe1059e812abb9c40cabce205273135d` |
| `2026-10-19_747fd256.raw.jsonl` | 979,349 | 221 | `7457d51c6e933703564a0105c435e66025d9d12d73ee496f52b409aa931c3cc6` |
| `2026-10-19_d80c799e.raw.jsonl` | 335,669 | 37 | `e67d24e2bbf8f01f201527eada60a34988fa7a6792dcfcf14cfc5fa04ec3f3bf` |
| `2026-10-19_ddac2ae1.raw.jsonl` | 638,231 | 48 | `bf723c6da59a81b0acc284f47022b09ae9dc5dab9d4e591a1e2887730ee3e2b7` |
| `2026-10-20_a1804bed.raw.jsonl` | 1,668,177 | 339 | `63e816e62939dc92dcfaeeff94f4332b0a4ced4b85157edd0e05eae639d01f80` |
| `2026-10-20_d14d6129.raw.jsonl` | 2,955,120 | 436 | `dc35ba08903fa1cb4f6b2d715d9c474e622ef402806a1f314e16e8fe1df848c3` |
| `2026-10-20_d5fe7447.raw.jsonl` | 624,098 | 58 | `4ed7af70a9d48c8735be9e0589d9f4b7179d5fd89cddc929d4ac915a1cd22937` |
| `2026-10-21_32907fd5.raw.jsonl` | 22,257 | 9 | `13dbe389a41ab2d041d1fb01b14098e1918e756ab9b4ccc00463ffd40d9ce997` |
| `2026-10-22_03cb0667.raw.jsonl` | 22,437 | 9 | `5792e26feafa53b01d0ffb377f0af6a83e9ded7def961bbf188401fc7e03c5e2` |
| `2026-10-22_750cb10e.raw.jsonl` | 1,990,702 | 615 | `9a606700d870f9fce2b715b570434590d34ce823a4ae44f94c4dadf1dc67856c` |
| `2026-10-22_bd788be5.raw.jsonl` | 2,401,340 | 593 | `77188e5ea4d1dfdc9f0abc6745558d32c4c450096b9942b79cfa2aefdb9c5ba4` |
| `2026-10-23_11662c2b.raw.jsonl` | 2,183,473 | 515 | `24b6693ecdd275fe87ecdfd7a62c6b8df1323a3c354f6491ee5eaa6e3fabd763` |
| `2026-10-23_24249c0f.raw.jsonl` | 771,451 | 78 | `afe9a3668068f6d612f610965a18a10db287c04077c897d1ed568f122e7c0f94` |
| `2026-10-23_34919197.raw.jsonl` | 2,306,017 | 742 | `66dbeebc38972306c69de046f202f462ab975444991c6a882a9db5b56eee9889` |
| `2026-10-25_32e10b59.raw.jsonl` | 505,292 | 40 | `231f74620b4e79ddc87fd7669b2a4bc8e32c502e62a3db1787e7066fd3afb7fe` |

## Codex CLI

_46 files, 473.9 MB, 8,363 records._

| File | Bytes | Records | SHA-256 |
|---|---|---|---|
| `2026-09-18_01a0b264.raw.jsonl` | 73,844,404 | 2,971 | `5b703138de9bf230e6885c40490ffccbb79b7582025ac9fae4aaa5647499878e` |
| `2026-09-18_01a0b275.raw.jsonl` | 190,570 | 43 | `ae9e8783989b1440177d55969434a93ee9815bb2b36c020610ec4ec3ca93a1fd` |
| `2026-09-21_01a0c437.raw.jsonl.gz` | 371,760,507 | compressed | `eeec8a83cccfdd88a3ccf151c2b244e3f29231012a18d9ec9149eafdf751f767` |
| `2026-09-22_01a0c909.raw.jsonl` | 2,362,078 | 114 | `e6a67b8b66bdb411537db4154befe4612a0ff46b3f771664c0f5dfe01356442c` |
| `2026-09-22_01a0c90d.raw.jsonl` | 3,618,446 | 74 | `7773ddb32526fa108ea365f9e8c276ff7a4875be25fe7ac179d509dd04877343` |
| `2026-09-22_01a0c92f.raw.jsonl` | 62,074 | 12 | `e90ab409fde9b5bf5ce502214e55df6071694520aeebb102254e9fa1432a260d` |
| `2026-09-22_01a0c952.raw.jsonl` | 867,708 | 83 | `3a1d12c7d478550aad6c3409c243dfa6669066a8eceaa5f9dd979a088fd6664e` |
| `2026-09-22_01a0c959.raw.jsonl` | 521,424 | 53 | `f35a51aded907365c4161a91be7ff9ae1f896440db938d18b29878eb6a9952f0` |
| `2026-09-22_01a0c9c3.raw.jsonl` | 765,663 | 49 | `46dd914df1103bc68784ebfeaef32c99a5f2dfd05f1d1acffde6dc2b401000f6` |
| `2026-09-22_01a0c9e6.raw.jsonl` | 88,794 | 17 | `e77407c304b34964d0d414072aea26cd64856d84caf7ffd0e68e8f5806e4fb88` |
| `2026-09-22_01a0ca1d.raw.jsonl` | 104,405 | 24 | `c20af6c171f506e9fd20a88de493b55ae0ecd1cbf6ae64beea1342c6048a72a3` |
| `2026-09-22_01a0cb66.raw.jsonl` | 2,031,879 | 141 | `48a1832ebe9654b4c2e9290375d7dbaa81dc8c82f76ac4b10fc2f0b9438bccab` |
| `2026-09-23_01a0cc37.raw.jsonl` | 445,787 | 35 | `81a69b6643b1428333372351b156f73f5a4761cdc2edcd271f46565a7ab8259c` |
| `2026-09-28_01a0e718.raw.jsonl` | 1,162,482 | 86 | `39a1b5ab06dfed6113ba66fefeae11b3c3a87d0516a7c266c7b72970fd128ed8` |
| `2026-09-28_01a0e71c.raw.jsonl` | 1,287,680 | 111 | `d4bcbc347da98d8ec6adf71e05c35b663fa48afebd38f9414c4b35f22bedfa48` |
| `2026-09-28_01a0e871.raw.jsonl` | 622,687 | 75 | `0cb1663bc883b76d13ede6bb91c5ad8ec8980150e5d919de911a536f136c4f63` |
| `2026-09-28_01a0e874.raw.jsonl` | 961,227 | 74 | `3215186fafda4b050b8833a996bd0060accc88d1169fd4f02f6d842331afa95a` |
| `2026-09-28_01a0e875.raw.jsonl` | 1,236,808 | 86 | `43b7e0d2226c70503cbaaa02df950f48f99d12962ca6f42b614891c8a6ec9261` |
| `2026-09-28_01a0e879.raw.jsonl` | 8,100,003 | 87 | `c75f532150d35033a65bfa1202b8349b437a3995e0ba058c16f3e27832aa3798` |
| `2026-09-28_01a0e87b.raw.jsonl` | 54,259 | 12 | `91efb100b136fb36068776457311ed9acb2129cb6759eaf89c9d2aeb498acff2` |
| `2026-09-28_01a0e881.raw.jsonl` | 55,858 | 12 | `3b302425ca6b4c3a6e4702b4f3e031c661625cd2d2d926f2cd6e0caeaea49992` |
| `2026-09-29_01a0eb6c.raw.jsonl` | 715,513 | 133 | `a8cfb54ee270df0428955b1579a6037283b9e2b7610aad257ac38543c8fab2ac` |
| `2026-09-29_01a0eb77.raw.jsonl` | 776,227 | 91 | `12c3507db3b3dcfcc6a747f1388c515d3e1fcfeebbb296a2692b96afd5249fba` |
| `2026-09-29_01a0eb7b.raw.jsonl` | 456,763 | 61 | `f8f2af26ff69bae4529d3189d6c0dbbdfdcdd47ff90b366f1ad5cb8c56ba6886` |
| `2026-09-29_01a0eb7d.raw.jsonl` | 59,198 | 12 | `888a40824350677392e7a2cbcab5b50756bd7f50532af8aa24b4b8d4523b27fd` |
| `2026-09-29_01a0ecb6.raw.jsonl` | 1,372,411 | 147 | `c4b182a58f560688760f1aad848f889b015971b8e3688d0b93d487e40571cc3e` |
| `2026-09-29_01a0ecbf.raw.jsonl` | 406,149 | 71 | `fce96a802bdadf477b07060e95a0b8d5fffb6566a26d521f32458f642d0af2d5` |
| `2026-09-29_01a0ecc1.raw.jsonl` | 245,620 | 47 | `33d7c53a5e2567a76cda80dac0c67cc06f029a623292bc6f21f1df88085ec238` |
| `2026-09-29_01a0ef37.raw.jsonl` | 303,979 | 59 | `be1fd97816b0fd5cdda8e7d78d0b751e553f899d91dbc01b5b68f168424e2f4c` |
| `2026-09-29_01a0ef39.raw.jsonl` | 574,279 | 57 | `993bb217e0d80509aabb9237bd71f01c24e3ffe0b77691eb1e0a876ceaf7fe93` |
| `2026-09-30_01a0f101.raw.jsonl` | 208,642 | 39 | `41e3ad5f98c45dae885e422a53acd2a3c29d63828d7bbd53e114b4ccf7f56be9` |
| `2026-10-09_01a12094.raw.jsonl` | 2,432,303 | 158 | `740caf382c2736495a6f357d9e58cadd8771443e5fe646161cfc18908f20523c` |
| `2026-10-09_01a120c1.raw.jsonl` | 56,439 | 12 | `92b751de5e9893170927670d96527994faf33004b7bec33d39c75cc9c5fbea71` |
| `2026-10-09_01a1215d.raw.jsonl` | 48,137 | 12 | `398f2891e0ec3f49b166fc91ba468ac355e006f3a86cdfe5c20f47c34a88a0f9` |
| `2026-10-13_01a13460.raw.jsonl` | 186,071 | 30 | `5b1a04522f4e78516f0aac1a9f527c1192d2f240b1c0c98868cc459eb836ae67` |
| `2026-10-14_01a137e8.raw.jsonl` | 197,791 | 36 | `6142d3f2616c144f6c4418561dbc20895cef2533d11c110e4ee62df82325011b` |
| `2026-10-14_01a13af8.raw.jsonl` | 236,806 | 36 | `bdff9f8bcdec7853018ac6baa920687242e1c3204d6cca9aaf07a0e7c8bde591` |
| `2026-10-19_01a15329.raw.jsonl` | 1,942,226 | 551 | `fd59a218f99d70b85e4b898ac5e01cada45a1328793bb6cff81726c10d783fcb` |
| `2026-10-20_01a156c4.raw.jsonl` | 4,473,523 | 732 | `adb063ff8cdcff5cd6b546f302575dedb02c36c099505280c457c724177715e3` |
| `2026-10-20_01a157f1.raw.jsonl` | 3,546,164 | 726 | `2c4775b9ffdff2eb046ec76ab4a06812dd05ca5d5ebd6c07e961ed3caa33961f` |
| `2026-10-23_01a166d0.raw.jsonl` | 425,619 | 46 | `53e145edc014cfe8b35315dbabb7ee3587da528f8248f8f2fc883115df975119` |
| `2026-10-23_01a166f6.raw.jsonl` | 349,202 | 43 | `444653a73d003164a0aa0fd487fc2b41b87f896b65b6b93d97f66f7501eea7e1` |
| `2026-10-23_01a168fb.raw.jsonl` | 1,250,775 | 268 | `3ce233c856ab001ac813fc2e88102f3d9a1bc3b62d944ac54a8bbad5fc1bbe80` |
| `2026-10-23_01a168fd.raw.jsonl` | 766,360 | 189 | `2d0bacecdb754ef62367fa30017b5b00aa87077b6ea677c0b01bfac6cc803879` |
| `2026-10-23_01a1690b.raw.jsonl` | 2,945,947 | 297 | `5af7878c606373a14b5722fccc8588552711f587ed8452b4a5bd1915bee24c01` |
| `2026-10-23_01a16a14.raw.jsonl` | 2,805,951 | 351 | `e16a302d8293bae699997aaa8370e6f1b466d45337765418c1bfcbd77f06b525` |

## Grok Bot

_16 files, 1.6 MB, 0 records._

| File | Bytes | Records | SHA-256 |
|---|---|---|---|
| `ALANA_full_transcript_raw_rows.json` | 596,719 | 0 | `76737ea3807c4f541c0ea36c5dd9e0b2116527f7b0667ef1d2d4d602d666689b` |
| `BOOK_EDITOR_2_full_transcript_raw_rows.json` | 15,517 | 0 | `4c5be43e35c0eb014d94071147af2d02130caf0caa219cf72a700ae35aa1b869` |
| `BOOK_EDITOR_full_transcript_raw_rows.json` | 697,858 | 0 | `af415a51698773ed38240f33a19e1037794131fd7db1785a1c27158f07671c78` |
| `COLD_READER_10_full_transcript_raw_rows.json` | 7,212 | 0 | `fb1d888ec91e9709807bad9143bdc180159b9459e184fb6e600cdafaeff0648f` |
| `COLD_READER_11_full_transcript_raw_rows.json` | 6,047 | 0 | `8d168fc72d06cff2ef87804e4980546470c535acd7c46a552a6905fac93fbc41` |
| `COLD_READER_2_full_transcript_raw_rows.json` | 25,855 | 0 | `23a813cd6a76ce14a2d7e9110c7d22335c644c7d33c8918abb928960d7b4db71` |
| `COLD_READER_3_full_transcript_raw_rows.json` | 34,512 | 0 | `88244a09aa9d7fd0df4a87b1c58e2af2b608c366f96ec54ee41171b9db41ad18` |
| `COLD_READER_4_full_transcript_raw_rows.json` | 67,420 | 0 | `99e3e48463a5828dd9d45bf581aa001c4c46f585106d73b9d90ef85e19488254` |
| `COLD_READER_5_full_transcript_raw_rows.json` | 5,854 | 0 | `7a9706d6d343d1fb7559413a700f77a8ee4d8f2b235892a3c9228c385fee62b0` |
| `COLD_READER_6_full_transcript_raw_rows.json` | 7,065 | 0 | `4d5b30cad36dba298b72023f422b5265654b1334df3480b69030ef5bdda8a7e0` |
| `COLD_READER_7_full_transcript_raw_rows.json` | 55,602 | 0 | `89ad75a8a2744669b5f3778d17e8b3c70a07195814a4f5f6f73fc1c28598325a` |
| `COLD_READER_9_full_transcript_raw_rows.json` | 11,893 | 0 | `d8e65e5656569b92adcd2adaf4408a0c7776dd75bac49812948c5621215dcd85` |
| `COLD_READER_full_transcript_raw_rows.json` | 26,362 | 0 | `6ed01f141e57c4bbfe50f5f945008e4566a788ca5894414be5ad936b54d5c946` |
| `COLD_READER_full_transcript_raw_rows_2026-10-02_2100.json` | 14,155 | 0 | `75d42d7e039e999cb7f215f03a4d3559ead2a501601f681717be71faf6a14efb` |
| `COVER_DESIGNER_full_transcript_raw_rows.json` | 48,098 | 0 | `1d50a7e7729791020b44c0ccfe43598f513a38d6a46c34059ca2f0b9282dd7e0` |
| `EDITOR_full_transcript_raw_rows_2026-09-30_SUPERSEDED.json` | 20,906 | 0 | `fffb5a9cec2d3e0e62f858057138cce029d8222ccf6bb2a0a109df04b63246de` |
