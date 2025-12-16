```mermaid
gantt
    title Open PDK and Design ? Timeline (from .gan)
    dateFormat  YYYY-MM-DD
    axisFormat  %Y-%m

    %% ---------------------------
    section Open PDK development
    Open PDK development (overall)         :active, opdk, 2022-06-01, 1028d
    Management open PDK development        :done,   opdk_mgmt, 2022-12-01, 780d
    Kick off (milestone)                   :milestone, opdk_kick, 2023-01-16, 0d

    section Internal test server
    Setup internal test server             :done,  its_setup, 2022-12-01, 180d
    Support internal test server           :active, its_support, 2023-08-16, 721d

    section GitHub support
    PDK basics ? Release GitHub (ms)       :milestone, gh_rel, 2023-03-03, 0d
    PDK update and user support on GitHub  :done,  gh_support, 2023-03-03, 716d
    Documentation build system (Open130-G2):done,  gh_docsys, 2023-12-01, 131d
    Evaluation of CI system                :done,  gh_ci_eval, 2023-11-02, 90d
    Implementation of CI system            :active, gh_ci_impl, 2024-05-13, 100d

    section Basic digital PDK in Open130-G2
    Basic digital PDK (overall)            :done,  dig, 2023-02-13, 316d
    Eval digital toolchain and IP          :done,  dig_eval, 2023-03-01, 21d
    Develop digital standard cells         :done,  dig_std, 2023-02-13, 79d
    Char first set of standard cells       :done,  dig_char1, 2023-03-15, 55d
    Develop IO cells                       :active, dig_io_dev, 2023-05-29, 90d
    Char IO cells                          :done,  dig_io_char, 2023-10-16, 90d
    Setup simple design example            :done,  dig_ex, 2023-08-01, 182d
    Release first Alpha PDK (ms)           :milestone, dig_alpha, 2024-05-13, 0d

    section PDK tool evaluation (Open130-G2)
    Tool evaluation (analog sim / DRC / LVS):done, tool_eval, 2023-02-01, 30d
    Model conversion for OS simulator      :done, model_conv, 2023-03-15, 150d
    HBT model conversion                   :done, hbt, 2023-03-15, 30d
    MOSFET model conversion                :done, mos, 2023-08-01, 30d
    Passive models conversion              :done, ???, 2023-06-08, 90d
    Models validation and testing          :done, val, 2023-09-04, 40d

    section Modeling and analog simulation
    Modeling and analog simulation (overall):active, ana, 2023-01-02, 653d
    EM simulation tools ? eval/adapt       :done, em_eval, 2023-01-02, 171d
    Interface for EM simulator             :done, em_if, 2023-10-02, 232d
    EM simulator optimization              :active, em_opt, 2024-09-02, 229d
    S-parameter simulation ? impl/test     :done, sparam, 2024-02-01, 86d
    Evaluation of Qucs-S                   :done, qucs, 2023-04-03, 160d

    section Analog PDK development
    Analog PDK development (overall)       :active, apdk, 2023-01-02, 759d
    Xschem symbols + testbenches library   :done, xsch, 2023-08-01, 103d
    Tool eval + basic layout features      :done, layout, 2023-02-01, 85d
    Update process specification           :done, proc, 2023-01-02, 64d
    Update DRM specification               :done, drm, 2023-03-01, 60d

    %% DRC stream
    section DRC rules
    Implementation basic DRC rules (overall):active, drc, 2023-06-01, 466d
    KLayout DRC implementation             :active, drc_kl, 2023-06-01, 221d
    Minimum required KLayout DRC rules     :active, drc_min, 2023-06-01, 65d
    Release mandatory KLayout DRC (ms)     :milestone, drc_rel, 2023-09-01, 0d
    Develop >=90% KLayout DRC rules        :done, drc_90, 2023-09-01, 134d
    KLayout DRC verification               :active, drc_ver, 2024-03-15, 22d

    Magic DRC implementation               :active, drc_mag, 2024-07-08, 187d
    Minimum required Magic DRC rules       :done, drc_mag_min, 2024-07-08, 65d
    Release mandatory Magic DRC (ms)       :milestone, drc_mag_rel, 2024-10-09, 0d
    Develop >=90% Magic DRC rules          :done, drc_mag_90, 2024-10-09, 100d
    Magic DRC verification                 :active, drc_mag_ver, 2025-03-06, 22d

    %% LVS stream
    section LVS rules
    Implementation basic LVS rules (overall):active, lvs, 2024-04-16, 432d
    KLayout LVS implementation             :active, lvs_kl, 2024-04-16, 135d
    LVS docs + test circuits               :done, lvs_docs, 2024-04-16, 65d
    Release LVS doc KLayout (ms)           :milestone, lvs_doc_rel, 2024-07-17, 0d
    Develop all KLayout LVS rules          :done, lvs_all, 2024-07-01, 60d
    KLayout LVS verification               :active, lvs_ver, 2024-09-24, 22d

    Magic LVS implementation               :active, lvs_mag, 2025-04-07, 187d
    Minimum required Magic LVS rules       :done, lvs_mag_min, 2025-04-07, 65d
    Release mandatory Magic LVS (ms)       :milestone, lvs_mag_rel, 2025-07-08, 0d
    Develop >=90% Magic LVS rules          :done, lvs_mag_90, 2025-07-08, 100d
    Magic LVS verification                 :active, lvs_mag_ver, 2025-11-28, 22d

    %% PCells + extraction
    section PCells and extraction
    PCell development (basic devices)      :active, pc, 2023-07-03, 564d
    Migration concept (PyCells -> KLayout) :done, pc_concept, 2023-07-03, 146d
    PyCells KLayout wrappers API           :done, pc_wrap, 2023-10-02, 60d
    Release initial migration concept (ms) :milestone, pc_ms, 2024-02-01, 0d

    PCell development in Magic             :active, pc_mag, 2025-04-07, 120d
    Minimum required Magic PCells          :done, pc_mag_min, 2025-04-07, 35d
    Release initial Magic PCells (ms)      :milestone, pc_mag_rel, 2025-05-27, 0d
    Develop >=90% Magic PCells             :done, pc_mag_90, 2025-05-27, 73d
    Magic PCells verification              :active, pc_mag_ver, 2025-09-08, 12d

    Evaluate parasitic extraction tools    :done, prx, 2025-01-02, 120d
    Analog Open Source PDK Alpha Release (ms):milestone, apdk_alpha, 2024-07-31, 0d

    %% ---------------------------
    section Tool interface development
    Tool interface development (overall)   :active, ti, 2023-04-12, 688d
    Eval analog toolchain interfaces       :done, ti_eval, 2023-04-12, 120d
    Library Manager interface              :done, libm, 2023-05-02, 120d
    Enhancements of Library Manager        :done, libm2, 2023-10-19, 555d
    Schematic-to-Layout interface          :done, s2l, 2023-12-18, 150d
    Layout-to-ParasiticExtraction interface:done, l2p, 2025-06-02, 148d
    Testing design tool interfaces         :done, ti_test, 2024-10-01, 314d
    PDK customization for continuous flow  :done, ti_flow, 2023-11-06, 545d
