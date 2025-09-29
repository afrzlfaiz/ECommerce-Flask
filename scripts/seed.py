import os, json, pathlib
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not (SUPABASE_URL and SERVICE_KEY):
    raise SystemExit("Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env")

sb = create_client(SUPABASE_URL, SERVICE_KEY)

def run_sql_file(path):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    # Run in SQL editor or via RPC; here we assume using pgsql connection is not available,
    # so we execute DDL pieces that PostgREST supports via /rest/v1/rpc isn't ideal.
    # As a workaround, print instructions and proceed to seed data.
    print(">>> Please paste sql/ddl_rls.sql into Supabase SQL editor and run it once.")
    return

def seed_products():
    sample = [
    {
        "id": "EIS-35743-08553",
        "name": "EIGER REVEAL 18 LAPTOP BACKPACK",
        "brand": "Eiger",
        "category": "Tas Ransel Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//95/MTA-94133525/eiger_eiger-reveal-18-laptop-backpack_full17.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/MTA-94133525/eiger_eiger_reveal_18_laptop_backpack_full02_gc5ng4sj.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/MTA-94133525/eiger_eiger_reveal_18_laptop_backpack_full01_qcwvidkg.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//95/MTA-94133525/eiger_eiger-reveal-18-laptop-backpack_full18.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//95/MTA-94133525/eiger_eiger-reveal-18-laptop-backpack_full19.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//95/MTA-94133525/eiger_eiger-reveal-18-laptop-backpack_full20.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//95/MTA-94133525/eiger_eiger-reveal-18-laptop-backpack_full21.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//95/MTA-94133525/eiger_eiger-reveal-18-laptop-backpack_full22.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//95/MTA-94133525/eiger_eiger-reveal-18-laptop-backpack_full23.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//95/MTA-94133525/eiger_eiger-reveal-18-laptop-backpack_full24.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/MTA-94133525/eiger_eiger_reveal_18_laptop_backpack_full03_qkrj1wr.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-94133525/eiger_eiger_reveal_18_laptop_backpack_full01_mg566dzq.jpg"
        ],
        "price": 367200.0,
        "discount": 20,
        "rating": 5.0,
        "review_count": 5,
        "sold_count": 72
    },
    {
        "id": "EIS-35743-09724",
        "name": "EIGER BOMBYX 18 NG BACKPACK",
        "brand": "Eiger",
        "category": "Tas Ransel Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full15_o4u1esur.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full08_s13lki1h.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full16_m0ja09wm.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full17_ch2rjz49.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full18_hy1lnxd3.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full19_iidi9chd.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full09_r4m52z1q.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full10_rrz1s08x.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full11_d4w7cajf.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full12_jfigfwqp.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full13_phxowwj3.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/99/MTA-154047518/eiger_eiger_bombyx_18_ng_backpack_full14_gdkovds8.jpg"
        ],
        "price": 335200.0,
        "discount": 20,
        "rating": 5.0,
        "review_count": 3,
        "sold_count": 14
    },
    {
        "id": "EIS-35743-08436",
        "name": "EIGER FORLOUGH 20 LAPTOP BACKPACK",
        "brand": "Eiger",
        "category": "Tas Ransel Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//102/MTA-93692118/eiger_eiger-forlough-20-laptop-backpack_full15.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93692118/eiger_eiger_forlough_20_laptop_backpack_full23_prqamyjg.jpeg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//102/MTA-93692118/eiger_eiger-forlough-20-laptop-backpack_full16.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//102/MTA-93692118/eiger_eiger-forlough-20-laptop-backpack_full17.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//102/MTA-93692118/eiger_eiger-forlough-20-laptop-backpack_full18.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//102/MTA-93692118/eiger_eiger-forlough-20-laptop-backpack_full19.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//102/MTA-93692118/eiger_eiger-forlough-20-laptop-backpack_full20.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//102/MTA-93692118/eiger_eiger-forlough-20-laptop-backpack_full21.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//102/MTA-93692118/eiger_eiger_forlough_20_laptop_backpack_full01_gk82ovjk.jpg"
        ],
        "price": 439200.0,
        "discount": 20,
        "rating": 5.0,
        "review_count": 5,
        "sold_count": 43
    },
    {
        "id": "EIS-35743-09960",
        "name": "EIGER ONE MAN RD T-SHIRT",
        "brand": "Eiger",
        "category": "T-Shirt Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-158929121/eiger_eiger_one_man_rd_t-shirt_full14_ctp2hndm.jpeg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-158929121/eiger_eiger_one_man_rd_t-shirt_full13_udm4sx2.jpeg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-158929121/eiger_eiger_one_man_rd_t-shirt_full12_kjk3z0td.jpeg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/101/MTA-158929121/eiger_eiger_full06.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/101/MTA-158929121/eiger_eiger_full07.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/101/MTA-158929121/eiger_eiger_full08.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/101/MTA-158929121/eiger_eiger_full9.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/101/MTA-158929121/eiger_eiger_full10.jpg"
        ],
        "price": 215200.0,
        "discount": 20,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-08255",
        "name": "EIGER GALI TRAVEL POUCH H 3L",
        "brand": "Eiger",
        "category": "Tas Selempang Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204859/eiger_eiger_gali_travel_pouch_h_3l_full02_kqoe3m2o.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//104/MTA-93204859/eiger_eiger_gali_travel_pouch_h_3l_full01_nemfg49k.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204859/eiger_eiger_gali_travel_pouch_h_3l_full01_ltiec97e.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204859/eiger_eiger_gali_travel_pouch_h_3l_full03_fuiwazdm.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204859/eiger_eiger_gali_travel_pouch_h_3l_full04_ehv7lysf.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204859/eiger_eiger_gali_travel_pouch_h_3l_full05_bvhzbo7v.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204859/eiger_eiger_gali_travel_pouch_h_3l_full06_vq8rhj3.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204859/eiger_eiger_gali_travel_pouch_h_3l_full07_mwoqlii6.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204859/eiger_eiger_gali_travel_pouch_h_3l_full08_jsymakhi.jpg"
        ],
        "price": 279000.0,
        "discount": 0,
        "rating": 5.0,
        "review_count": 6,
        "sold_count": 14
    },
    {
        "id": "EIS-35743-11088",
        "name": "EIGER STRATO JOGGER PANTS",
        "brand": "Eiger",
        "category": "Celana Jogger Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/120/MTA-166982889/eiger_eiger_full01.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/120/MTA-166982889/eiger_eiger_full06.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/120/MTA-166982889/eiger_eiger_full07.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/120/MTA-166982889/eiger_eiger_full05.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/120/MTA-166982889/eiger_eiger_full03.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/120/MTA-166982889/eiger_eiger_full04.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/120/MTA-166982889/eiger_eiger_full02.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-166982889/eiger_eiger_strato_jogger_pants_full01_kvkm8s6t.jpg"
        ],
        "price": 436050.0,
        "discount": 5,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-08567",
        "name": "EIGER X-CORDYLINE WALLET 1.0",
        "brand": "Eiger",
        "category": "Dompet Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//99/MTA-94133628/eiger_eiger-x-cordyline-wallet-1-0_full04.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//99/MTA-94133628/eiger_eiger_x-cordyline_wallet_1-0_full01_fjsr3tz5.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//99/MTA-94133628/eiger_eiger-x-cordyline-wallet-1-0_full05.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//99/MTA-94133628/eiger_eiger-x-cordyline-wallet-1-0_full06.jpg"
        ],
        "price": 56050.0,
        "discount": 5,
        "rating": 4.8,
        "review_count": 46,
        "sold_count": 302
    },
    {
        "id": "EIS-35743-11105",
        "name": "EIGER WANDERER POUCH 1A",
        "brand": "Eiger",
        "category": "Tas Selempang Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/109/MTA-166990329/eiger_eiger_wanderer_pouch_1a_full14_s5g2l0s3.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/109/MTA-166990329/eiger_eiger_wanderer_pouch_1a_full15_tuty0cw6.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/109/MTA-166990329/eiger_eiger_wanderer_pouch_1a_full16_sj4oynj4.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/109/MTA-166990329/eiger_eiger_wanderer_pouch_1a_full17_vz1ggn61.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/109/MTA-166990329/eiger_eiger_wanderer_pouch_1a_full18_dvm2m7fv.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/109/MTA-166990329/eiger_eiger_wanderer_pouch_1a_full19_riyjl3lj.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/109/MTA-166990329/eiger_eiger_wanderer_pouch_1a_full20_iyqms5if.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/109/MTA-166990329/eiger_eiger_wanderer_pouch_1a_full21_un854yj3.jpg"
        ],
        "price": 255200.0,
        "discount": 20,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-13195",
        "name": "EIGER EVREDAIT SS T-SHIRT",
        "brand": "Eiger",
        "category": "Baju Kasual",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-182650453/eiger_eiger_evredait_ss_t-shirt_full01_bn6voo8h.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-182650453/eiger_eiger_evredait_ss_t-shirt_full02_r1aseqlf.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-182650453/eiger_eiger_evredait_ss_t-shirt_full03_guyrd4uy.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-182650453/eiger_eiger_evredait_ss_t-shirt_full04_s23xgu4z.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-182650453/eiger_eiger_evredait_ss_t-shirt_full05_ua8zgyqd.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-182650453/eiger_eiger_evredait_ss_t-shirt_full06_s88n5pze.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-182650453/eiger_eiger_evredait_ss_t-shirt_full07_spj1z6ya.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-182650453/eiger_eiger_evredait_ss_t-shirt_full08_qw3mp22q.jpg"
        ],
        "price": 189000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-10018",
        "name": "EIGER C.1989 FREE WAY PANTS",
        "brand": "Eiger",
        "category": "Celana Kasual Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-158931081/eiger_eiger_c-1989_free_way_pants_full15_v4io88ju.jpeg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-158931081/eiger_eiger_c-1989_free_way_pants_full14_t6meky61.jpeg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-158931081/eiger_eiger_full07.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-158931081/eiger_eiger_full08.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-158931081/eiger_eiger_full9.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-158931081/eiger_eiger_full10.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-158931081/eiger_eiger_full11.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-158931081/eiger_eiger_c-1989_free_way_pants_full01_evjnx6up.jpg"
        ],
        "price": 335200.0,
        "discount": 20,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 1
    },
    {
        "id": "EIS-35743-09629",
        "name": "EIGER X-JOURNAL PACK 20L 1A LAPTOP BACKPACK",
        "brand": "Eiger",
        "category": "Tas Ransel Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-143542642/eiger_eiger_x-journal_pack_20l_1a_laptop_backpack_full02_ba088qfn.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/94/MTA-143542642/eiger_eiger_x-journal_pack_20l_1a_laptop_backpack_full02_n38i9oc.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/94/MTA-143542642/eiger_eiger_x-journal_pack_20l_1a_laptop_backpack_full03_ia9o2kai.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/94/MTA-143542642/eiger_eiger_x-journal_pack_20l_1a_laptop_backpack_full04_ptyufiwv.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/94/MTA-143542642/eiger_eiger_x-journal_pack_20l_1a_laptop_backpack_full05_elbh8tfj.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/94/MTA-143542642/eiger_eiger_x-journal_pack_20l_1a_laptop_backpack_full06_s3g1dbzf.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/94/MTA-143542642/eiger_eiger_x-journal_pack_20l_1a_laptop_backpack_full07_fr0i5yez.jpg"
        ],
        "price": 359200.0,
        "discount": 20,
        "rating": 5.0,
        "review_count": 1,
        "sold_count": 2
    },
    {
        "id": "EIS-35743-09802",
        "name": "EIGER 12C-6048 BASEBALL CAP",
        "brand": "Eiger",
        "category": "Topi & Bandana",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-158674443/eiger_eiger_12c-6048_baseball_cap_full01_c0r6voul.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-158674443/eiger_eiger_12c-6048_baseball_cap_full02_jc7lyt2w.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-158674443/eiger_eiger_12c-6048_baseball_cap_full03_rkj308vo.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-158674443/eiger_eiger_12c-6048_baseball_cap_full04_sb3q8rxy.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-158674443/eiger_eiger_12c-6048_baseball_cap_full05_odl9gfnh.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-158674443/eiger_eiger_12c-6048_baseball_cap_full06_bxtblav4.jpg"
        ],
        "price": 127200.0,
        "discount": 20,
        "rating": 5.0,
        "review_count": 1,
        "sold_count": 1
    },
    {
        "id": "ONL-70041-07275",
        "name": "Kupluk Eiger Kanchenjunga 6936",
        "brand": "Eiger",
        "category": "Topi & Bandana",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-154049970/br-m036969-04893_kupluk-eiger-kanchenjunga-6936-_full01-75a54bb7.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-154049970/br-m036969-04893_kupluk-eiger-kanchenjunga-6936-_full02-6d92e9b2.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-154049970/br-m036969-04893_kupluk-eiger-kanchenjunga-6936-_full03-aa26ab63.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-154049970/br-m036969-04893_kupluk-eiger-kanchenjunga-6936-_full04-21627c44.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-154049970/br-m036969-04893_kupluk-eiger-kanchenjunga-6936-_full05-b114437f.jpg"
        ],
        "price": 190400.0,
        "discount": 27,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-13213",
        "name": "EIGER EVREDAIT BUCKET HAT",
        "brand": "Eiger",
        "category": "Topi & Bandana",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182665781/eiger_eiger_evredait_bucket_hat_full08_jcqcosxm.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182665781/eiger_eiger_evredait_bucket_hat_full01_mfbihzxb.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182665781/eiger_eiger_evredait_bucket_hat_full02_is1tarqn.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182665781/eiger_eiger_evredait_bucket_hat_full03_rsl3w0n5.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182665781/eiger_eiger_evredait_bucket_hat_full04_tt5kxbr.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182665781/eiger_eiger_evredait_bucket_hat_full05_sbryueml.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182665781/eiger_eiger_evredait_bucket_hat_full06_evc0stht.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182665781/eiger_eiger_evredait_bucket_hat_full07_mywjx367.jpg"
        ],
        "price": 199000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-13201",
        "name": "EIGER JUNIOR PHRAYA PINCH STRAP SANDALS",
        "brand": "Eiger",
        "category": "Sandal Anak Laki",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/110/MTA-182652959/eiger_eiger_junior_phraya_pinch_strap_sandals_full08_haajrilv.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/110/MTA-182652959/eiger_eiger_junior_phraya_pinch_strap_sandals_full01_vma9qzds.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/110/MTA-182652959/eiger_eiger_junior_phraya_pinch_strap_sandals_full02_txo8b33s.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/110/MTA-182652959/eiger_eiger_junior_phraya_pinch_strap_sandals_full03_jl9euxnz.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/110/MTA-182652959/eiger_eiger_junior_phraya_pinch_strap_sandals_full04_ulalszfx.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/110/MTA-182652959/eiger_eiger_junior_phraya_pinch_strap_sandals_full05_uwzsh8wp.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/110/MTA-182652959/eiger_eiger_junior_phraya_pinch_strap_sandals_full06_erdylynl.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/110/MTA-182652959/eiger_eiger_junior_phraya_pinch_strap_sandals_full07_l1n436mz.jpg"
        ],
        "price": 189000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-13084",
        "name": "EIGER PULSE TRAIL MEN 2.0 SHOES",
        "brand": "Eiger",
        "category": "Sepatu Kasual",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/86/MTA-182300150/eiger_eiger_pulse_trail_men_2-0_shoes_full04_k7310kix.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/86/MTA-182300150/eiger_eiger_pulse_trail_men_2-0_shoes_full01_qso57juq.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/86/MTA-182300150/eiger_eiger_pulse_trail_men_2-0_shoes_full02_d9jveiiz.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/86/MTA-182300150/eiger_eiger_pulse_trail_men_2-0_shoes_full03_icif1jgq.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/86/MTA-182300150/eiger_eiger_pulse_trail_men_2-0_shoes_full05_we5tfa3w.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/86/MTA-182300150/eiger_eiger_pulse_trail_men_2-0_shoes_full06_uadr13di.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/86/MTA-182300150/eiger_eiger_pulse_trail_men_2-0_shoes_full07_l3q5mn0p.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/86/MTA-182300150/eiger_eiger_pulse_trail_men_2-0_shoes_full08_mtretcgs.jpg"
        ],
        "price": 1281550.0,
        "discount": 5,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-13144",
        "name": "EIGER COROPUNA CAP",
        "brand": "Eiger",
        "category": "Topi & Bandana",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182529145/eiger_eiger_coropuna_cap_full08_qh6lrpx4.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182529145/eiger_eiger_coropuna_cap_full01_vcfmv82l.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182529145/eiger_eiger_coropuna_cap_full02_m6em1hot.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182529145/eiger_eiger_coropuna_cap_full03_ei6rrldm.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182529145/eiger_eiger_coropuna_cap_full04_b2nij438.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182529145/eiger_eiger_coropuna_cap_full05_lqb3j8du.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182529145/eiger_eiger_coropuna_cap_full06_cot1g499.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182529145/eiger_eiger_coropuna_cap_full07_nxo7enx.jpg"
        ],
        "price": 199000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-13193",
        "name": "EIGER TURCO LS T-SHIRT",
        "brand": "Eiger",
        "category": "Baju Kasual",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182649760/eiger_eiger_turco_ls_t-shirt_full01_piy7dfrs.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182649760/eiger_eiger_turco_ls_t-shirt_full02_d6cnqmi4.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182649760/eiger_eiger_turco_ls_t-shirt_full03_gak348xa.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182649760/eiger_eiger_turco_ls_t-shirt_full04_vb7psyvh.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182649760/eiger_eiger_turco_ls_t-shirt_full05_l1nwgxw8.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182649760/eiger_eiger_turco_ls_t-shirt_full06_mu24r034.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182649760/eiger_eiger_turco_ls_t-shirt_full07_v7sim0mb.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/107/MTA-182649760/eiger_eiger_turco_ls_t-shirt_full08_wdcyw14d.jpg"
        ],
        "price": 249000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-13203",
        "name": "EIGER WOMEN DAICY MID CUT 1.0 SOCKS",
        "brand": "Eiger",
        "category": "Kaos Kaki Wanita",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182657642/eiger_eiger_women_daicy_mid_cut_1-0_socks_full04_vhdu26ac.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182657642/eiger_eiger_women_daicy_mid_cut_1-0_socks_full01_r014moho.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182657642/eiger_eiger_women_daicy_mid_cut_1-0_socks_full02_vf2cu46z.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182657642/eiger_eiger_women_daicy_mid_cut_1-0_socks_full03_p4cr1j8r.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182657642/eiger_eiger_women_daicy_mid_cut_1-0_socks_full05_tecy2w54.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182657642/eiger_eiger_women_daicy_mid_cut_1-0_socks_full06_cbzxx03z.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182657642/eiger_eiger_women_daicy_mid_cut_1-0_socks_full07_hxtepiub.jpg"
        ],
        "price": 59000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-13140",
        "name": "EIGER WEEKURI WATER BOTTLE 700ML",
        "brand": "Eiger",
        "category": "Gelas & Perangkat Minum",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full01_b90zq5rk.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full02_mq1eg2ff.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full03_uxx1ocr2.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full04_lqnsni1.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full05_qrmbqz5l.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full06_hbcxaqar.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full07_f3io7mb5.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full08_gzk56ihv.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full09_cq2n6ie1.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full10_grgh4tfp.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full11_8i1g679.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-182528184/eiger_eiger_weekuri_water_bottle_700ml_full12_dyqbraaz.jpg"
        ],
        "price": 129000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-08417",
        "name": "EIGER HARRIER SHOES",
        "brand": "Eiger",
        "category": "Sepatu Lari",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93692093/eiger_eiger_harrier_shoes_full06_p7570w24.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//105/MTA-93692093/eiger_eiger_harrier_shoes_full01_u49p35mq.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93692093/eiger_eiger_harrier_shoes_full01_ovac5f8t.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93692093/eiger_eiger_harrier_shoes_full02_ns3v0tw0.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93692093/eiger_eiger_harrier_shoes_full03_siq1nnco.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93692093/eiger_eiger_harrier_shoes_full04_fp741eku.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93692093/eiger_eiger_harrier_shoes_full05_t4vyw0ef.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93692093/eiger_eiger_harrier_shoes_full07_h49ul6h7.jpg"
        ],
        "price": 1359000.0,
        "discount": 0,
        "rating": 5.0,
        "review_count": 2,
        "sold_count": 4
    },
    {
        "id": "EIS-35743-13066",
        "name": "EIGER TALA SLIP ON SANDALS",
        "brand": "Eiger",
        "category": "Sandal Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182275336/eiger_eiger_tala_slip_on_sandals_full07_wd3nwwp7.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182275336/eiger_eiger_tala_slip_on_sandals_full01_u935heev.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182275336/eiger_eiger_tala_slip_on_sandals_full02_t8oliowh.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182275336/eiger_eiger_tala_slip_on_sandals_full03_uoo4vjlw.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182275336/eiger_eiger_tala_slip_on_sandals_full04_ku3noavm.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182275336/eiger_eiger_tala_slip_on_sandals_full05_tccleqtn.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182275336/eiger_eiger_tala_slip_on_sandals_full06_kvj0jc9e.jpg"
        ],
        "price": 369000.0,
        "discount": 0,
        "rating": 5.0,
        "review_count": 2,
        "sold_count": 2
    },
    {
        "id": "EIS-35743-13183",
        "name": "EIGER X-KUGA SS T-SHIRT RX",
        "brand": "Eiger",
        "category": "Baju Kasual",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/97/MTA-182625054/eiger_eiger_x-kuga_ss_t-shirt_rx_full04_mqrzyxza.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/97/MTA-182625054/eiger_eiger_x-kuga_ss_t-shirt_rx_full01_uid6p746.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/97/MTA-182625054/eiger_eiger_x-kuga_ss_t-shirt_rx_full02_f74mxnax.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/97/MTA-182625054/eiger_eiger_x-kuga_ss_t-shirt_rx_full03_besfa4oo.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/97/MTA-182625054/eiger_eiger_x-kuga_ss_t-shirt_rx_full05_fb6otnf0.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/97/MTA-182625054/eiger_eiger_x-kuga_ss_t-shirt_rx_full06_du68j2nn.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/97/MTA-182625054/eiger_eiger_x-kuga_ss_t-shirt_rx_full07_nw9846j4.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/97/MTA-182625054/eiger_eiger_x-kuga_ss_t-shirt_rx_full08_focumxnn.jpg"
        ],
        "price": 199000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-11573",
        "name": "EIGER BARRIER DOPP KIT 1A",
        "brand": "Eiger",
        "category": "Clutch Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full02_efgm35gk.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full07_cls5y54p.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full01_hcbt1vjw.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full02_m5gtgcfn.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full03_mmmtszzz.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full04_g8mflvwi.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full05_u2cxzi85.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full06_dl2wk67f.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full01_q6ejq1w4.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full03_kyz9obrc.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full04_o08753ov.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full05_iifuz9u8.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full06_hw688f1d.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-178601443/eiger_eiger_barrier_dopp_kit_1a_full07_sk96fpmb.jpg"
        ],
        "price": 219000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 2
    },
    {
        "id": "EIS-35743-12324",
        "name": "EIGER HILLWANDER DOPP KIT",
        "brand": "Eiger",
        "category": "Clutch Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180357801/eiger_eiger_hillwander_dopp_kit_full01_c9ygugy9.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-180357801/eiger_eiger_hillwander_dopp_kit_full09_kpjmvcf8.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/98/MTA-180357801/eiger_eiger_hillwander_dopp_kit_full08_bhe3wr8e.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180357801/eiger_eiger_hillwander_dopp_kit_full02_h1brelsm.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180357801/eiger_eiger_hillwander_dopp_kit_full03_iw11v9pe.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180357801/eiger_eiger_hillwander_dopp_kit_full04_c1qeth7v.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180357801/eiger_eiger_hillwander_dopp_kit_full05_is7sttbm.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180357801/eiger_eiger_hillwander_dopp_kit_full06_b7rea385.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180357801/eiger_eiger_hillwander_dopp_kit_full07_m40ugpqk.jpg"
        ],
        "price": 179000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-12261",
        "name": "EIGER SAFAR LOW CUT SHOES",
        "brand": "Eiger",
        "category": "Sepatu Kasual",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180353567/eiger_eiger_safar_low_cut_shoes_full07_tku9af89.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180353567/eiger_eiger_safar_low_cut_shoes_full01_q5s4mo8o.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180353567/eiger_eiger_safar_low_cut_shoes_full02_uelak839.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180353567/eiger_eiger_safar_low_cut_shoes_full03_27hkugl.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180353567/eiger_eiger_safar_low_cut_shoes_full04_jm04zazn.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180353567/eiger_eiger_safar_low_cut_shoes_full05_c0ldu70c.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180353567/eiger_eiger_safar_low_cut_shoes_full06_d733ie6j.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-180353567/eiger_eiger_safar_low_cut_shoes_full08_pqb8viks.jpg"
        ],
        "price": 629100.0,
        "discount": 10,
        "rating": 5.0,
        "review_count": 1,
        "sold_count": 1
    },
    {
        "id": "EIS-35743-13162",
        "name": "EIGER COASTICO BELT POUCH",
        "brand": "Eiger",
        "category": "Tas Pinggang Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full32_42ma92d.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full30_u4l0gkz4.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full31_mqi4bgd4.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full33_mf3f4v09.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full34_c172kiqa.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full35_d0zidf2i.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full36_h37nozhg.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full37_tztix7qo.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full22_vvb07710.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full23_t6nwug30.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full24_lrtw8q1z.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full25_dyqsjnp5.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full26_myeryia1.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full27_rg1xug1o.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full28_smobwq9p.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/88/MTA-182550001/eiger_eiger_coastico_belt_pouch_full29_rpo8g0ep.jpg"
        ],
        "price": 135200.0,
        "discount": 20,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-09139",
        "name": "EIGER REVENNA KEYCHAIN WALLET WS",
        "brand": "Eiger",
        "category": "Dompet Wanita",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/MTA-118646229/eiger_eiger_revenna_keychain_wallet_ws_full08_i2jhkdmi.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/102/MTA-118646229/eiger_eiger_revenna_keychain_wallet_ws_full02_o1iclyyn.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/102/MTA-118646229/eiger_eiger_revenna_keychain_wallet_ws_full03_sxcfv0d8.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/102/MTA-118646229/eiger_eiger_revenna_keychain_wallet_ws_full04_hsj6xlyd.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/102/MTA-118646229/eiger_eiger_revenna_keychain_wallet_ws_full05_q9d8b9oi.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/102/MTA-118646229/eiger_eiger_revenna_keychain_wallet_ws_full06_dx1l8g9h.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/MTA-118646229/eiger_eiger_revenna_keychain_wallet_ws_full07_nrfgjc82.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/MTA-118646229/eiger_eiger_revenna_keychain_wallet_ws_full09_n78hj2xe.jpg"
        ],
        "price": 69000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 1
    },
    {
        "id": "EIS-35743-13207",
        "name": "EIGER ESSENTIAL SS SHIRT RX",
        "brand": "Eiger",
        "category": "Kemeja Formal Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/92/MTA-182661301/eiger_eiger_essential_ss_shirt_rx_full01_gfhj6sfk.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/92/MTA-182661301/eiger_eiger_essential_ss_shirt_rx_full02_lr2bvmtl.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/92/MTA-182661301/eiger_eiger_essential_ss_shirt_rx_full03_fsd6a531.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/92/MTA-182661301/eiger_eiger_essential_ss_shirt_rx_full04_sk057oxq.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/92/MTA-182661301/eiger_eiger_essential_ss_shirt_rx_full05_qdnbwr8k.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/92/MTA-182661301/eiger_eiger_essential_ss_shirt_rx_full06_s6u4dj0s.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/92/MTA-182661301/eiger_eiger_essential_ss_shirt_rx_full07_orw68etr.jpg"
        ],
        "price": 349000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-13185",
        "name": "EIGER X- BANSKA POLOSHIRT LS",
        "brand": "Eiger",
        "category": "Kaos Polo Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182628186/eiger_eiger_x-_banska_poloshirt_ls_full02_wjp8ockw.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182628186/eiger_eiger_x-_banska_poloshirt_ls_full01_jgr90h0f.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182628186/eiger_eiger_x-_banska_poloshirt_ls_full03_bai9uiqz.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182628186/eiger_eiger_x-_banska_poloshirt_ls_full04_hpmlrxvl.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182628186/eiger_eiger_x-_banska_poloshirt_ls_full05_hhsemoqi.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182628186/eiger_eiger_x-_banska_poloshirt_ls_full06_il4q0wk1.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182628186/eiger_eiger_x-_banska_poloshirt_ls_full07_fq5jr41.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182628186/eiger_eiger_x-_banska_poloshirt_ls_full08_ukffxnwg.jpg"
        ],
        "price": 309000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-13166",
        "name": "EIGER MORTY SS T-SHIRT RX",
        "brand": "Eiger",
        "category": "T-Shirt Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182557170/eiger_eiger_morty_ss_t-shirt_rx_full08_m58on6zu.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182557170/eiger_eiger_morty_ss_t-shirt_rx_full01_rcqjlqce.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182557170/eiger_eiger_morty_ss_t-shirt_rx_full02_p6dtj2u.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182557170/eiger_eiger_morty_ss_t-shirt_rx_full03_kgeletg4.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182557170/eiger_eiger_morty_ss_t-shirt_rx_full04_dlbgp31n.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182557170/eiger_eiger_morty_ss_t-shirt_rx_full05_tye6soz5.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182557170/eiger_eiger_morty_ss_t-shirt_rx_full06_e6jjyksi.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/100/MTA-182557170/eiger_eiger_morty_ss_t-shirt_rx_full07_cxqvce0c.jpg"
        ],
        "price": 239000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-08256",
        "name": "EIGER KARLSKOGA WATCH",
        "brand": "Eiger",
        "category": "Jam Tangan Digital Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//97/MTA-93204861/eiger_eiger-karlskoga-watch_full01.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/MTA-93204861/eiger_eiger_karlskoga_watch_full01_b6d0mesw.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//97/MTA-93204861/eiger_eiger-karlskoga-watch_full02.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//97/MTA-93204861/eiger_eiger-karlskoga-watch_full03.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//97/MTA-93204861/eiger_eiger-karlskoga-watch_full04.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//97/MTA-93204861/eiger_eiger-karlskoga-watch_full05.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//97/MTA-93204861/eiger_eiger-karlskoga-watch_full06.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//catalog-image/MTA-93204861/eiger_eiger_karlskoga_watch_full02_tmet2qem.jpg"
        ],
        "price": 549000.0,
        "discount": 0,
        "rating": 5.0,
        "review_count": 6,
        "sold_count": 91
    },
    {
        "id": "EIS-35743-08314",
        "name": "EIGER TRAVERSE 23 1.0 BACKPACK",
        "brand": "Eiger",
        "category": "Tas Ransel Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full01_s6nssb86.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//98/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full01_52focpi.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full01_ncm7j3p2.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full02_qvqg0h9v.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full03_dmb1lw2v.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full04_nmjgzqhh.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full05_c8ar5ipu.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full06_fpn43af6.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full02_9x3wck3.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full03_k0926lij.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full04_hv0yron0.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full05_l9rfma3a.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full06_ijib7s01.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93205068/eiger_eiger_traverse_23_1-0_backpack_full07_kfkiq50u.jpg"
        ],
        "price": 489000.0,
        "discount": 0,
        "rating": 5.0,
        "review_count": 4,
        "sold_count": 25
    },
    {
        "id": "EIS-35743-13048",
        "name": "EIGER VERTMOUNTRIDE HOODIE SWEATER",
        "brand": "Eiger",
        "category": "Jaket & Hoodies",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/94/MTA-182265510/eiger_eiger_vertmountride_hoodie_sweater_full08_jj152ee5.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/94/MTA-182265510/eiger_eiger_vertmountride_hoodie_sweater_full01_cmruezxq.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/94/MTA-182265510/eiger_eiger_vertmountride_hoodie_sweater_full02_vsl0g96o.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/94/MTA-182265510/eiger_eiger_vertmountride_hoodie_sweater_full03_hy67edn1.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/94/MTA-182265510/eiger_eiger_vertmountride_hoodie_sweater_full04_h0lep1pv.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/94/MTA-182265510/eiger_eiger_vertmountride_hoodie_sweater_full05_tijnfwc9.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/94/MTA-182265510/eiger_eiger_vertmountride_hoodie_sweater_full06_jh831ffr.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/94/MTA-182265510/eiger_eiger_vertmountride_hoodie_sweater_full07_zmj3fcr.jpg"
        ],
        "price": 519000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-08207",
        "name": "EIGER STINGRAY 1.0 SHOES",
        "brand": "Eiger",
        "category": "Sepatu Kasual",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204717/eiger_eiger_stingray_1-0_shoes_full01_ne3hfrcx.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//97/MTA-93204717/eiger_eiger_stingray_1-0_shoes_full01_bgiz7rup.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204717/eiger_eiger_stingray_1-0_shoes_full01_cimu694e.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204717/eiger_eiger_stingray_1-0_shoes_full02_eqsycayi.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204717/eiger_eiger_stingray_1-0_shoes_full03_fzws3zj1.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204717/eiger_eiger_stingray_1-0_shoes_full04_mm4e149t.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204717/eiger_eiger_stingray_1-0_shoes_full05_rsl5em8h.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-93204717/eiger_eiger_stingray_1-0_shoes_full06_e5wa05s.jpg"
        ],
        "price": 879200.0,
        "discount": 20,
        "rating": 5.0,
        "review_count": 2,
        "sold_count": 4
    },
    {
        "id": "EIS-35743-12891",
        "name": "EIGER VERTMOUNTRIDE DIGITAL POUCH",
        "brand": "Eiger",
        "category": "Clutch Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182008677/eiger_eiger_vertmountride_digital_pouch_full08_tvcuperp.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182008677/eiger_eiger_vertmountride_digital_pouch_full09_dnn75po7.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182008677/eiger_eiger_vertmountride_digital_pouch_full10_ojirei2e.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182008677/eiger_eiger_vertmountride_digital_pouch_full11_m2ntd2r3.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182008677/eiger_eiger_vertmountride_digital_pouch_full12_e91ohn4k.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182008677/eiger_eiger_vertmountride_digital_pouch_full13_u3hbt9hh.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182008677/eiger_eiger_vertmountride_digital_pouch_full14_veft17jh.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/104/MTA-182008677/eiger_eiger_vertmountride_digital_pouch_full15_o2xnkrim.jpg"
        ],
        "price": 239000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-13125",
        "name": "EIGER X-VERTIC JOGGER PANTS",
        "brand": "Eiger",
        "category": "Celana Jogger Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/102/MTA-182465292/eiger_eiger_x-vertic_jogger_pants_full08_qsj54ao4.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/102/MTA-182465292/eiger_eiger_x-vertic_jogger_pants_full01_qz3t6x1.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/102/MTA-182465292/eiger_eiger_x-vertic_jogger_pants_full02_b35jp4r2.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/102/MTA-182465292/eiger_eiger_x-vertic_jogger_pants_full03_nlsuw3ts.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/102/MTA-182465292/eiger_eiger_x-vertic_jogger_pants_full04_cqsgvkt5.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/102/MTA-182465292/eiger_eiger_x-vertic_jogger_pants_full05_k2gs9qe4.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/102/MTA-182465292/eiger_eiger_x-vertic_jogger_pants_full06_lfsq1j1g.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/102/MTA-182465292/eiger_eiger_x-vertic_jogger_pants_full07_emaivpdt.jpg"
        ],
        "price": 489000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    },
    {
        "id": "EIS-35743-10840",
        "name": "EIGER VISAYAS MEN SANDALS",
        "brand": "Eiger",
        "category": "Sandal Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-162043533/eiger_eiger_visayas_men_sandals_full03_uoprd9qx.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/91/MTA-162043533/eiger_eiger-visayas-men-sandals_full01.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/91/MTA-162043533/eiger_eiger-visayas-men-sandals_full06.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/91/MTA-162043533/eiger_eiger-visayas-men-sandals_full04.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/91/MTA-162043533/eiger_eiger-visayas-men-sandals_full03.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/91/MTA-162043533/eiger_eiger-visayas-men-sandals_full02.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-162043533/eiger_eiger_visayas_men_sandals_full01_8fj16tk.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-162043533/eiger_eiger_visayas_men_sandals_full02_jm8qebr4.jpg"
        ],
        "price": 160550.0,
        "discount": 5,
        "rating": 5.0,
        "review_count": 9,
        "sold_count": 22
    },
    {
        "id": "EIS-35743-10398",
        "name": "EIGER SATTLER SUNGLASSES",
        "brand": "Eiger",
        "category": "Kacamata Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/MTA-158982031/eiger_eiger_sattler_sunglasses_full01_qa4j7yho.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/101/MTA-158982031/eiger_eiger-sattler-sunglasses_full01.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/101/MTA-158982031/eiger_eiger-sattler-sunglasses_full02.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/101/MTA-158982031/eiger_eiger-sattler-sunglasses_full03.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/101/MTA-158982031/eiger_eiger-sattler-sunglasses_full04.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/101/MTA-158982031/eiger_eiger-sattler-sunglasses_full05.jpg"
        ],
        "price": 265050.0,
        "discount": 5,
        "rating": 5.0,
        "review_count": 2,
        "sold_count": 9
    },
    {
        "id": "EIS-35743-13121",
        "name": "EIGER RIVULET POUCH BAG 1A",
        "brand": "Eiger",
        "category": "Tas Selempang Pria",
        "images": [
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182462397/eiger_eiger_rivulet_pouch_bag_1a_full02_i486k6lz.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182462397/eiger_eiger_rivulet_pouch_bag_1a_full01_s1q70ccg.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182462397/eiger_eiger_rivulet_pouch_bag_1a_full03_mjh7yza6.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182462397/eiger_eiger_rivulet_pouch_bag_1a_full04_iewox3qf.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182462397/eiger_eiger_rivulet_pouch_bag_1a_full05_ljpz8q1i.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182462397/eiger_eiger_rivulet_pouch_bag_1a_full06_lvvjtvli.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182462397/eiger_eiger_rivulet_pouch_bag_1a_full07_brqrt7s9.jpg",
        "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/catalog-image/105/MTA-182462397/eiger_eiger_rivulet_pouch_bag_1a_full08_upzy33yy.jpg"
        ],
        "price": 209000.0,
        "discount": 0,
        "rating": 0.0,
        "review_count": 0,
        "sold_count": 0
    }
    ]
    sb.table("products").upsert(sample).execute()
    print("Seeded products:", len(sample))

def create_admin(email: str, password: str):
    # Create or get user
    try:
        resp = sb.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {},
            "app_metadata": {"role":"admin"}
        })
        user = resp.user
    except Exception as e:
        print("admin create_user error (maybe exists):", e)
        # Try to find user by email
        user = None
        try:
            users = sb.auth.admin.list_users()
            for u in users.data:
                if u.email == email:
                    user = u
                    break
        except Exception as e2:
            print("list_users error:", e2)
    if user:
        try:
            sb.auth.admin.update_user_by_id(user.id, {"app_metadata": {"role":"admin"}})
            print("Admin ensured with role=admin:", user.id)
        except Exception as e:
            print("update_user_by_id error:", e)

if __name__ == "__main__":
    print("== Seeding ==")
    run_sql_file(str(pathlib.Path(__file__).resolve().parents[1] / "sql" / "ddl_rls.sql"))
    seed_products()
    # Change these credentials
    create_admin("kelompokecommerce@gmailot.com", "Passw0rd!")
    print("Done")
