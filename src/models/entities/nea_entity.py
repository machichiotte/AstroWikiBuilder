# src/models/entities/nea_entity.py
# Mapping des colonnes NEA vers les attributs Star
from dataclasses import dataclass


@dataclass
class NEA_ENTITY:
    """Classe représentant l'objet recu par api depuis Nasa Exoplanet Archive"""

    objectid: str | None = None
    pl_name: str | None = None
    pl_letter: str | None = None
    hostid: str | None = None
    hostname: str | None = None
    hd_name: str | None = None
    hip_name: str | None = None
    tic_id: str | None = None
    disc_pubdate: str | None = None
    disc_year: str | None = None
    disc_method: str | None = None
    discoverymethod: str | None = None
    disc_locale: str | None = None
    disc_facility: str | None = None
    disc_instrument: str | None = None
    disc_telescope: str | None = None
    disc_refname: str | None = None
    ra: str | None = None
    raerr1: str | None = None
    raerr2: str | None = None
    rasymerr: str | None = None
    rastr: str | None = None
    ra_solnid: str | None = None
    ra_reflink: str | None = None
    dec: str | None = None
    decerr1: str | None = None
    decerr2: str | None = None
    decsymerr: str | None = None
    decstr: str | None = None
    dec_solnid: str | None = None
    dec_reflink: str | None = None
    glon: str | None = None
    glonerr1: str | None = None
    glonerr2: str | None = None
    glonsymerr: str | None = None
    glonstr: str | None = None
    glon_solnid: str | None = None
    glon_reflink: str | None = None
    glat: str | None = None
    glaterr1: str | None = None
    glaterr2: str | None = None
    glatsymerr: str | None = None
    glatstr: str | None = None
    glat_solnid: str | None = None
    glat_reflink: str | None = None
    elon: str | None = None
    elonerr1: str | None = None
    elonerr2: str | None = None
    elonsymerr: str | None = None
    elonstr: str | None = None
    elon_solnid: str | None = None
    elon_reflink: str | None = None
    elat: str | None = None
    elaterr1: str | None = None
    elaterr2: str | None = None
    elatsymerr: str | None = None
    elat_solnid: str | None = None
    elat_reflink: str | None = None
    elatstr: str | None = None
    pl_orbper: str | None = None
    pl_orbpererr1: str | None = None
    pl_orbpererr2: str | None = None
    pl_orbpersymerr: str | None = None
    pl_orbperlim: str | None = None
    pl_orbperstr: str | None = None
    pl_orbperformat: str | None = None
    pl_orbper_solnid: str | None = None
    pl_orbper_reflink: str | None = None
    pl_orblpererr1: str | None = None
    pl_orblper: str | None = None
    pl_orblpererr2: str | None = None
    pl_orblpersymerr: str | None = None
    pl_orblperlim: str | None = None
    pl_orblperstr: str | None = None
    pl_orblperformat: str | None = None
    pl_orblper_solnid: str | None = None
    pl_orblper_reflink: str | None = None
    pl_orbsmax: str | None = None
    pl_orbsmaxerr1: str | None = None
    pl_orbsmaxerr2: str | None = None
    pl_orbsmaxsymerr: str | None = None
    pl_orbsmaxlim: str | None = None
    pl_orbsmaxstr: str | None = None
    pl_orbsmaxformat: str | None = None
    pl_orbsmax_solnid: str | None = None
    pl_orbsmax_reflink: str | None = None
    pl_orbincl: str | None = None
    pl_orbinclerr1: str | None = None
    pl_orbinclerr2: str | None = None
    pl_orbinclsymerr: str | None = None
    pl_orbincllim: str | None = None
    pl_orbinclstr: str | None = None
    pl_orbinclformat: str | None = None
    pl_orbincl_solnid: str | None = None
    pl_orbincl_reflink: str | None = None
    pl_orbtper: str | None = None
    pl_orbtpererr1: str | None = None
    pl_orbtpererr2: str | None = None
    pl_orbtpersymerr: str | None = None
    pl_orbtperlim: str | None = None
    pl_orbtperstr: str | None = None
    pl_orbtperformat: str | None = None
    pl_orbtper_solnid: str | None = None
    pl_orbtper_reflink: str | None = None
    pl_orbeccen: str | None = None
    pl_orbeccenerr1: str | None = None
    pl_orbeccenerr2: str | None = None
    pl_orbeccensymerr: str | None = None
    pl_orbeccenlim: str | None = None
    pl_orbeccenstr: str | None = None
    pl_orbeccenformat: str | None = None
    pl_orbeccen_solnid: str | None = None
    pl_orbeccen_reflink: str | None = None
    pl_eqt: str | None = None
    pl_eqterr1: str | None = None
    pl_eqterr2: str | None = None
    pl_eqtsymerr: str | None = None
    pl_eqtlim: str | None = None
    pl_eqtstr: str | None = None
    pl_eqtformat: str | None = None
    pl_eqt_solnid: str | None = None
    pl_eqt_reflink: str | None = None
    pl_occdep: str | None = None
    pl_occdeperr1: str | None = None
    pl_occdeperr2: str | None = None
    pl_occdepsymerr: str | None = None
    pl_occdeplim: str | None = None
    pl_occdepstr: str | None = None
    pl_occdepformat: str | None = None
    pl_occdep_solnid: str | None = None
    pl_occdep_reflink: str | None = None
    pl_insol: str | None = None
    pl_insolerr1: str | None = None
    pl_insolerr2: str | None = None
    pl_insolsymerr: str | None = None
    pl_insollim: str | None = None
    pl_insolstr: str | None = None
    pl_insolformat: str | None = None
    pl_insol_solnid: str | None = None
    pl_insol_reflink: str | None = None
    pl_dens: str | None = None
    pl_denserr1: str | None = None
    sy_umagerr1: str | None = None
    sy_umagerr2: str | None = None
    sy_umaglim: str | None = None
    sy_umagsymerr: str | None = None
    sy_umagstr: str | None = None
    sy_umagformat: str | None = None
    sy_umag_solnid: str | None = None
    sy_umag_reflink: str | None = None
    sy_rmag: str | None = None
    sy_rmagerr1: str | None = None
    sy_rmagerr2: str | None = None
    sy_rmaglim: str | None = None
    sy_rmagsymerr: str | None = None
    sy_rmagstr: str | None = None
    sy_rmagformat: str | None = None
    sy_rmag_solnid: str | None = None
    sy_rmag_reflink: str | None = None
    sy_imag: str | None = None
    sy_imagerr1: str | None = None
    sy_imagerr2: str | None = None
    sy_imaglim: str | None = None
    sy_imagsymerr: str | None = None
    sy_imagstr: str | None = None
    sy_imagformat: str | None = None
    sy_imag_solnid: str | None = None
    sy_imag_reflink: str | None = None
    sy_zmag: str | None = None
    sy_zmagerr1: str | None = None
    sy_zmagerr2: str | None = None
    sy_zmaglim: str | None = None
    sy_zmagsymerr: str | None = None
    sy_zmagstr: str | None = None
    sy_zmagformat: str | None = None
    sy_zmag_solnid: str | None = None
    sy_zmag_reflink: str | None = None
    sy_w1mag: str | None = None
    sy_w1magerr1: str | None = None
    sy_w1magerr2: str | None = None
    sy_w1maglim: str | None = None
    sy_w1magsymerr: str | None = None
    sy_w1magstr: str | None = None
    sy_w1magformat: str | None = None
    sy_w1mag_solnid: str | None = None
    sy_w1mag_reflink: str | None = None
    sy_w2mag: str | None = None
    sy_w2magerr1: str | None = None
    sy_w2magerr2: str | None = None
    sy_w2maglim: str | None = None
    sy_w2magsymerr: str | None = None
    sy_w2magstr: str | None = None
    sy_w2magformat: str | None = None
    sy_w2mag_solnid: str | None = None
    sy_w2mag_reflink: str | None = None
    sy_w3mag: str | None = None
    sy_w3magerr1: str | None = None
    sy_w3magerr2: str | None = None
    sy_w3maglim: str | None = None
    sy_w3magsymerr: str | None = None
    sy_w3magstr: str | None = None
    sy_w3magformat: str | None = None
    sy_w3mag_solnid: str | None = None
    sy_w3mag_reflink: str | None = None
    sy_w4mag: str | None = None
    sy_w4magerr1: str | None = None
    sy_w4magerr2: str | None = None
    sy_w4maglim: str | None = None
    sy_w4magsymerr: str | None = None
    sy_w4magstr: str | None = None
    sy_w4magformat: str | None = None
    sy_w4mag_solnid: str | None = None
    sy_w4mag_reflink: str | None = None
    sy_gmag: str | None = None
    sy_gmagerr1: str | None = None
    sy_gmagerr2: str | None = None
    sy_gmaglim: str | None = None
    sy_gmagsymerr: str | None = None
    sy_gmagstr: str | None = None
    sy_gmagformat: str | None = None
    sy_gmag_solnid: str | None = None
    sy_gmag_reflink: str | None = None
    sy_gaiamag: str | None = None
    sy_gaiamagerr1: str | None = None
    sy_gaiamagerr2: str | None = None
    sy_gaiamaglim: str | None = None
    sy_gaiamagsymerr: str | None = None
    sy_gaiamagstr: str | None = None
    sy_gaiamagformat: str | None = None
    sy_gaiamag_solnid: str | None = None
    sy_gaiamag_reflink: str | None = None
    sy_tmag: str | None = None
    sy_tmagerr1: str | None = None
    sy_tmagerr2: str | None = None
    sy_tmaglim: str | None = None
    sy_tmagsymerr: str | None = None
    sy_tmagstr: str | None = None
    sy_tmagformat: str | None = None
    sy_tmag_solnid: str | None = None
    sy_tmag_reflink: str | None = None
    sy_name: str | None = None
    pl_controv_flag: str | None = None
    pl_orbtper_systemref: str | None = None
    pl_tranmid_systemref: str | None = None
    st_metratio: str | None = None
    st_spectype: str | None = None
    st_spectype_solnid: str | None = None
    st_spectype_reflink: str | None = None
    sy_plxlim: str | None = None
    sy_kepmag: str | None = None
    sy_kepmagerr1: str | None = None
    sy_kepmagerr2: str | None = None
    sy_kepmaglim: str | None = None
    sy_kepmagsymerr: str | None = None
    sy_kepmagstr: str | None = None
    sy_kepformat: str | None = None
    sy_kepmag_solnid: str | None = None
    sy_kepmag_reflink: str | None = None
    st_rotp: str | None = None
    st_rotperr1: str | None = None
    st_rotperr2: str | None = None
    st_rotpsymerr: str | None = None
    st_rotplim: str | None = None
    st_rotpstr: str | None = None
    st_rotpformat: str | None = None
    st_rotp_solnid: str | None = None
    st_rotp_reflink: str | None = None
    pl_projobliq: str | None = None
    pl_projobliqerr1: str | None = None
    pl_projobliqerr2: str | None = None
    pl_projobliqsymerr: str | None = None
    pl_projobliqlim: str | None = None
    pl_projobliqstr: str | None = None
    pl_projobliqformat: str | None = None
    pl_denserr2: str | None = None
    pl_denssymerr: str | None = None
    pl_denslim: str | None = None
    pl_densstr: str | None = None
    pl_densformat: str | None = None
    pl_dens_solnid: str | None = None
    pl_dens_reflink: str | None = None
    pl_trandep: str | None = None
    pl_trandeperr1: str | None = None
    pl_trandeperr2: str | None = None
    pl_trandepsymerr: str | None = None
    pl_trandeplim: str | None = None
    pl_trandepstr: str | None = None
    pl_trandepformat: str | None = None
    pl_trandep_solnid: str | None = None
    pl_trandep_reflink: str | None = None
    pl_tranmid: str | None = None
    pl_tranmiderr1: str | None = None
    pl_tranmiderr2: str | None = None
    pl_tranmidsymerr: str | None = None
    pl_tranmidlim: str | None = None
    pl_tranmidstr: str | None = None
    pl_tranmidformat: str | None = None
    pl_tranmid_solnid: str | None = None
    pl_tranmid_reflink: str | None = None
    pl_trandur: str | None = None
    pl_trandurerr1: str | None = None
    pl_trandurerr2: str | None = None
    pl_trandursymerr: str | None = None
    pl_trandurlim: str | None = None
    pl_trandurstr: str | None = None
    pl_trandurformat: str | None = None
    pl_trandur_solnid: str | None = None
    pl_trandur_reflink: str | None = None
    pl_rvamp: str | None = None
    pl_rvamperr1: str | None = None
    pl_rvamperr2: str | None = None
    pl_rvampsymerr: str | None = None
    pl_rvamplim: str | None = None
    pl_rvampstr: str | None = None
    pl_rvampformat: str | None = None
    pl_rvamp_solnid: str | None = None
    pl_rvamp_reflink: str | None = None
    pl_radj: str | None = None
    pl_radjerr1: str | None = None
    pl_radjerr2: str | None = None
    pl_radjsymerr: str | None = None
    pl_radjlim: str | None = None
    pl_radjstr: str | None = None
    pl_radjformat: str | None = None
    pl_radj_solnid: str | None = None
    pl_radj_reflink: str | None = None
    pl_rade: str | None = None
    pl_radeerr1: str | None = None
    pl_radeerr2: str | None = None
    pl_radesymerr: str | None = None
    pl_radelim: str | None = None
    pl_radestr: str | None = None
    pl_radeformat: str | None = None
    pl_rade_solnid: str | None = None
    pl_rade_reflink: str | None = None
    pl_ratror: str | None = None
    pl_ratrorerr1: str | None = None
    pl_ratrorerr2: str | None = None
    pl_ratrorsymerr: str | None = None
    pl_ratrorlim: str | None = None
    pl_ratrorstr: str | None = None
    pl_ratrorformat: str | None = None
    pl_ratror_solnid: str | None = None
    pl_ratror_reflink: str | None = None
    pl_ratdor: str | None = None
    pl_trueobliq: str | None = None
    pl_trueobliqerr1: str | None = None
    pl_trueobliqerr2: str | None = None
    pl_trueobliqsymerr: str | None = None
    pl_trueobliqlim: str | None = None
    pl_trueobliqstr: str | None = None
    pl_trueobliqformat: str | None = None
    pl_trueobliq_solnid: str | None = None
    pl_trueobliq_reflink: str | None = None
    st_log_rhk: str | None = None
    st_log_rhkerr1: str | None = None
    st_log_rhkerr2: str | None = None
    st_log_rhksymerr: str | None = None
    st_log_rhklim: str | None = None
    st_log_rhkstr: str | None = None
    st_log_rhkformat: str | None = None
    st_log_rhk_solnid: str | None = None
    st_log_rhk_reflink: str | None = None
    st_metn: str | None = None
    sy_icmag: str | None = None
    sy_icmagerr1: str | None = None
    sy_icmagerr2: str | None = None
    sy_icmagsymerr: str | None = None
    sy_icmagstr: str | None = None
    sy_icmagformat: str | None = None
    sy_icmag_solnid: str | None = None
    sy_icmag_reflink: str | None = None
    pl_pubdate: str | None = None
    dkin_flag: str | None = None
    pl_ratdorerr1: str | None = None
    pl_ratdorerr2: str | None = None
    pl_ratdorsymerr: str | None = None
    pl_ratdorlim: str | None = None
    pl_ratdorstr: str | None = None
    pl_ratdorformat: str | None = None
    pl_ratdor_solnid: str | None = None
    pl_ratdor_reflink: str | None = None
    pl_imppar: str | None = None
    pl_impparerr1: str | None = None
    pl_impparerr2: str | None = None
    pl_impparsymerr: str | None = None
    pl_impparlim: str | None = None
    pl_impparstr: str | None = None
    pl_impparformat: str | None = None
    pl_imppar_solnid: str | None = None
    pl_imppar_reflink: str | None = None
    pl_cmassj: str | None = None
    pl_cmassjerr1: str | None = None
    pl_cmassjerr2: str | None = None
    pl_cmassjsymerr: str | None = None
    pl_cmassjlim: str | None = None
    pl_cmassjstr: str | None = None
    pl_cmassjformat: str | None = None
    pl_cmassj_solnid: str | None = None
    pl_cmassj_reflink: str | None = None
    pl_cmasse: str | None = None
    pl_cmasseerr1: str | None = None
    pl_cmasseerr2: str | None = None
    pl_cmassesymerr: str | None = None
    pl_cmasselim: str | None = None
    pl_cmassestr: str | None = None
    pl_cmasseformat: str | None = None
    pl_cmasse_solnid: str | None = None
    pl_cmasse_reflink: str | None = None
    pl_massj: str | None = None
    pl_massjerr1: str | None = None
    pl_massjerr2: str | None = None
    pl_massjsymerr: str | None = None
    pl_massjlim: str | None = None
    pl_massjstr: str | None = None
    pl_massjformat: str | None = None
    pl_massj_solnid: str | None = None
    pl_massj_reflink: str | None = None
    pl_masse: str | None = None
    pl_masseerr1: str | None = None
    pl_masseerr2: str | None = None
    pl_massesymerr: str | None = None
    pl_masselim: str | None = None
    pl_massestr: str | None = None
    pl_masseformat: str | None = None
    pl_masse_solnid: str | None = None
    pl_masse_reflink: str | None = None
    pl_bmassj: str | None = None
    pl_bmassjerr1: str | None = None
    pl_bmassjerr2: str | None = None
    pl_bmassjsymerr: str | None = None
    pl_bmassjlim: str | None = None
    pl_bmassjstr: str | None = None
    pl_bmassjformat: str | None = None
    pl_bmassj_solnid: str | None = None
    pl_bmassj_reflink: str | None = None
    pl_bmasse: str | None = None
    pl_bmasseerr1: str | None = None
    pl_bmasseerr2: str | None = None
    pl_bmassesymerr: str | None = None
    pl_bmasselim: str | None = None
    pl_bmassestr: str | None = None
    pl_bmasseformat: str | None = None
    pl_bmasse_solnid: str | None = None
    pl_bmasse_reflink: str | None = None
    pl_bmassprov: str | None = None
    pl_msinij: str | None = None
    pl_msinijerr1: str | None = None
    pl_msinijerr2: str | None = None
    pl_msinijsymerr: str | None = None
    pl_msinijlim: str | None = None
    pl_msinijstr: str | None = None
    pl_msinijformat: str | None = None
    pl_msinij_solnid: str | None = None
    pl_msinij_reflink: str | None = None
    pl_msinie: str | None = None
    pl_msinieerr1: str | None = None
    pl_msinieerr2: str | None = None
    pl_msiniesymerr: str | None = None
    pl_msinielim: str | None = None
    pl_msiniestr: str | None = None
    pl_msinieformat: str | None = None
    pl_msinie_solnid: str | None = None
    pl_msinie_reflink: str | None = None
    st_teff: str | None = None
    st_tefferr1: str | None = None
    st_tefferr2: str | None = None
    st_teffsymerr: str | None = None
    st_tefflim: str | None = None
    st_teffstr: str | None = None
    st_teffformat: str | None = None
    st_teff_solnid: str | None = None
    st_teff_reflink: str | None = None
    st_met: str | None = None
    st_meterr1: str | None = None
    st_meterr2: str | None = None
    st_metsymerr: str | None = None
    st_metlim: str | None = None
    st_metstr: str | None = None
    st_metformat: str | None = None
    st_met_solnid: str | None = None
    st_met_reflink: str | None = None
    st_radv: str | None = None
    st_radverr1: str | None = None
    st_radverr2: str | None = None
    st_radvsymerr: str | None = None
    st_radvlim: str | None = None
    st_radvstr: str | None = None
    st_radvformat: str | None = None
    st_radv_solnid: str | None = None
    st_radv_reflink: str | None = None
    st_vsin: str | None = None
    st_vsinerr1: str | None = None
    st_vsinerr2: str | None = None
    st_vsinsymerr: str | None = None
    st_vsinlim: str | None = None
    st_vsinstr: str | None = None
    st_vsin_solnid: str | None = None
    st_vsin_reflink: str | None = None
    st_vsinformat: str | None = None
    st_lum: str | None = None
    st_lumerr1: str | None = None
    st_lumerr2: str | None = None
    st_lumsymerr: str | None = None
    st_lumlim: str | None = None
    st_lumstr: str | None = None
    st_lumformat: str | None = None
    st_lum_solnid: str | None = None
    st_lum_reflink: str | None = None
    st_logg: str | None = None
    st_loggerr1: str | None = None
    st_loggerr2: str | None = None
    st_loggsymerr: str | None = None
    st_logglim: str | None = None
    st_loggstr: str | None = None
    st_loggformat: str | None = None
    st_logg_solnid: str | None = None
    st_logg_reflink: str | None = None
    st_age: str | None = None
    st_ageerr1: str | None = None
    st_ageerr2: str | None = None
    st_agesymerr: str | None = None
    st_agelim: str | None = None
    st_agestr: str | None = None
    st_ageformat: str | None = None
    st_age_solnid: str | None = None
    st_age_reflink: str | None = None
    st_mass: str | None = None
    st_masserr1: str | None = None
    st_masserr2: str | None = None
    st_masssymerr: str | None = None
    st_masslim: str | None = None
    st_massstr: str | None = None
    st_massformat: str | None = None
    st_mass_solnid: str | None = None
    st_mass_reflink: str | None = None
    st_dens: str | None = None
    st_denserr1: str | None = None
    st_denserr2: str | None = None
    st_denssymerr: str | None = None
    st_denslim: str | None = None
    st_densstr: str | None = None
    st_densformat: str | None = None
    st_dens_solnid: str | None = None
    st_dens_reflink: str | None = None
    st_rad: str | None = None
    st_raderr1: str | None = None
    st_raderr2: str | None = None
    st_radsymerr: str | None = None
    st_radlim: str | None = None
    st_radstr: str | None = None
    st_radformat: str | None = None
    st_rad_solnid: str | None = None
    st_rad_reflink: str | None = None
    systemid: str | None = None
    ttv_flag: str | None = None
    ptv_flag: str | None = None
    tran_flag: str | None = None
    rv_flag: str | None = None
    ast_flag: str | None = None
    obm_flag: str | None = None
    micro_flag: str | None = None
    etv_flag: str | None = None
    ima_flag: str | None = None
    pul_flag: str | None = None
    disc_refid: str | None = None
    sy_snum: str | None = None
    sy_pnum: str | None = None
    sy_mnum: str | None = None
    st_nphot: str | None = None
    st_nrvc: str | None = None
    st_nspec: str | None = None
    pl_nespec: str | None = None
    pl_ntranspec: str | None = None
    pl_nnotes: str | None = None
    sy_pm: str | None = None
    sy_pmerr1: str | None = None
    sy_pmerr2: str | None = None
    sy_pmsymerr: str | None = None
    sy_pmlim: str | None = None
    sy_pmstr: str | None = None
    sy_pmformat: str | None = None
    sy_pm_solnid: str | None = None
    sy_pm_reflink: str | None = None
    sy_pmra: str | None = None
    sy_pmraerr1: str | None = None
    sy_pmraerr2: str | None = None
    sy_pmrasymerr: str | None = None
    sy_pmralim: str | None = None
    sy_pmrastr: str | None = None
    sy_pmraformat: str | None = None
    sy_pmra_solnid: str | None = None
    sy_pmra_reflink: str | None = None
    sy_pmdec: str | None = None
    sy_pmdecerr1: str | None = None
    sy_pmdecerr2: str | None = None
    sy_pmdecsymerr: str | None = None
    sy_pmdeclim: str | None = None
    sy_pmdecstr: str | None = None
    sy_pmdecformat: str | None = None
    sy_pmdec_solnid: str | None = None
    sy_pmdec_reflink: str | None = None
    sy_plx: str | None = None
    sy_plxerr1: str | None = None
    sy_plxerr2: str | None = None
    sy_plxsymerr: str | None = None
    sy_plxstr: str | None = None
    sy_plxformat: str | None = None
    sy_plx_solnid: str | None = None
    sy_plx_reflink: str | None = None
    sy_dist: str | None = None
    sy_disterr1: str | None = None
    sy_disterr2: str | None = None
    sy_distsymerr: str | None = None
    sy_distlim: str | None = None
    sy_diststr: str | None = None
    sy_distformat: str | None = None
    sy_dist_solnid: str | None = None
    sy_dist_reflink: str | None = None
    sy_bmag: str | None = None
    sy_bmagerr1: str | None = None
    sy_bmagerr2: str | None = None
    sy_bmaglim: str | None = None
    sy_bmagsymerr: str | None = None
    sy_bmagstr: str | None = None
    sy_bmagformat: str | None = None
    sy_bmag_solnid: str | None = None
    sy_bmag_reflink: str | None = None
    sy_vmag: str | None = None
    sy_vmagerr1: str | None = None
    sy_vmagerr2: str | None = None
    sy_vmaglim: str | None = None
    sy_vmagsymerr: str | None = None
    sy_vmagstr: str | None = None
    sy_vmagformat: str | None = None
    sy_vmag_solnid: str | None = None
    sy_vmag_reflink: str | None = None
    sy_jmag: str | None = None
    sy_jmagerr1: str | None = None
    sy_jmagerr2: str | None = None
    sy_jmaglim: str | None = None
    sy_jmagsymerr: str | None = None
    sy_jmagstr: str | None = None
    sy_jmagformat: str | None = None
    sy_jmag_solnid: str | None = None
    sy_jmag_reflink: str | None = None
    sy_hmag: str | None = None
    sy_hmagerr1: str | None = None
    sy_hmagerr2: str | None = None
    sy_hmaglim: str | None = None
    sy_hmagsymerr: str | None = None
    sy_hmagstr: str | None = None
    sy_hmagformat: str | None = None
    sy_hmag_solnid: str | None = None
    sy_hmag_reflink: str | None = None
    sy_kmag: str | None = None
    sy_kmagerr1: str | None = None
    sy_kmagerr2: str | None = None
    sy_kmaglim: str | None = None
    sy_kmagsymerr: str | None = None
    sy_kmagstr: str | None = None
    sy_kmagformat: str | None = None
    sy_kmag_solnid: str | None = None
    sy_kmag_reflink: str | None = None
    sy_umag: str | None = None
    pl_projobliq_solnid: str | None = None
    pl_projobliq_reflink: str | None = None
    x: str | None = None
    y: str | None = None
    z: str | None = None
    htm20: str | None = None
    gaia_id: str | None = None
    cb_flag: str | None = None
    pl_angsep: str | None = None
    pl_angseperr1: str | None = None
    pl_angseperr2: str | None = None
    pl_angseplim: str | None = None
    pl_angsepformat: str | None = None
    pl_angsepstr: str | None = None
    pl_angsepsymerr: str | None = None
    pl_angsep_reflink: str | None = None
    pl_ndispec: str | None = None


NEA_TO_STAR_MAPPING = {
    # Identifiants
    "hostname": "st_name",
    # Coordonnées
    "ra": "st_right_ascension",
    "dec": "st_declination",
    "sy_pmra": "st_proper_motion_ra",
    "sy_pmdec": "st_proper_motion_dec",
    "sy_plx": "st_parallax",
    "sy_dist": "st_distance",
    # Magnitudes
    "sy_bmag": "st_mag_b",
    "sy_vmag": "st_mag_v",
    "sy_jmag": "st_mag_j",
    "sy_hmag": "st_mag_h",
    "sy_kmag": "st_mag_k",
    "sy_gmag": "st_mag_g",
    "sy_rmag": "st_mag_r",
    "sy_imag": "st_mag_i",
    "sy_umag": "st_mag_u",
    "sy_zmag": "st_mag_z",
    "sy_w1mag": "st_mag_w1",
    "sy_w2mag": "st_mag_w2",
    "sy_w3mag": "st_mag_w3",
    "sy_w4mag": "st_mag_w4",
    "sy_gaiamag": "st_mag_gaia",
    "sy_tmag": "st_mag_t",
    "sy_kepmag": "st_mag_kep",
    # Propriétés stellaires
    "st_teff": "st_temperature",
    "st_mass": "st_mass",
    "st_rad": "st_radius",
    "st_met": "st_metallicity",
    "st_logg": "st_surface_gravity",
    "st_lum": "st_luminosity",
    "st_dens": "st_density",
    "st_age": "st_age",
    "st_spectype": "st_spectral_type",
    "st_radv": "st_radial_velocity",
    "st_rotp": "st_rotation",
}

# Mapping des colonnes NEA vers les attributs Exoplanet
NEA_TO_EXOPLANET_MAPPING = {
    "pl_name": "pl_name",
    "pl_altname": "pl_altname",
    "hostname": "st_name",
    "st_spectype": "st_spectral_type",
    "sy_dist": "st_distance",
    "sy_vmag": "st_apparent_magnitude",
    "pl_orbsmax": "pl_semi_major_axis",
    "pl_orbeccen": "pl_eccentricity",
    "pl_orbper": "pl_orbital_period",
    "pl_angsep": "pl_angular_distance",
    "pl_orbtper": "pl_periastron_time",
    "pl_orbincl": "pl_inclination",
    "pl_orblper": "pl_argument_of_periastron",
    "pl_bmassj": "pl_mass",
    "pl_msinij": "pl_minimum_mass",
    "pl_radj": "pl_radius",
    "pl_dens": "pl_density",
    "pl_eqt": "pl_temperature",
    "discoverymethod": "disc_method",
    "disc_year": "disc_year",
    "disc_facility": "disc_facility",
    "st_mass": "st_mass",
    "st_met": "st_metallicity",
    "st_age": "st_age",
    "pl_insol": "pl_insolation_flux",
    "pl_trandep": "pl_transit_depth",
    "sy_pnum": "sy_planet_count",
}

# Unités par défaut pour certains champs NEA
NEA_DEFAULT_UNITS: dict[str, str] = {
    # --- Coordonnées et mouvements ---
    "ra": "°",  # Ascension droite
    "dec": "°",  # Déclinaison
    "sy_pmra": "mas/an",  # mouvement propre en RA
    "sy_pmdec": "mas/an",  # mouvement propre en DEC
    "sy_plx": "mas",  # parallaxe
    "sy_dist": "pc",  # parsecs
    # --- Étoile (préfixe st_) ---
    "st_teff": "K",  # Température effective
    "st_mass": "M☉",  # Masse stellaire
    "st_rad": "R☉",  # Rayon stellaire
    "st_met": "[Fe/H]",  # Métallicité (dex mais exprimée [Fe/H])
    "st_logg": "log g",  # Gravité de surface log g
    "st_lum": "L☉",  # Luminosité stellaire
    "st_dens": "g/cm³",  # Densité stellaire
    "st_age": "Ga",  # Âge stellaire
    "st_radv": "km/s",  # Vitesse radiale
    "st_rotp": "j",  # Période de rotation (jours)
    "st_vsin": "km/s",  # Vitesse de rotation projetée
    # --- Planète (préfixe pl_) ---
    "pl_orbper": "j",  # Période orbitale (jours)
    "pl_angsep": "″",  # Séparation angulaire (arcsec)
    "pl_orbincl": "°",  # Inclinaison orbitale
    "pl_msinij": "MJ",  # Masse minimum (Jupiter)
    "pl_bmassj": "MJ",  # Masse brute (Jupiter)
    "pl_radj": "RJ",  # Rayon (Jupiter)
    "pl_dens": "g/cm³",  # Densité planétaire
    "pl_eqt": "K",  # Température d'équilibre
}
