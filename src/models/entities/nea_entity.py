# src/models/entities/nea_entity.py
# Mapping des colonnes NEA vers les attributs Star
from dataclasses import dataclass
from typing import Optional


@dataclass
class NEA_ENTITY:
    """Classe représentant l'objet recu par api depuis Nasa Exoplanet Archive"""

    objectid: Optional[str] = None
    pl_name: Optional[str] = None
    pl_letter: Optional[str] = None
    hostid: Optional[str] = None
    hostname: Optional[str] = None
    hd_name: Optional[str] = None
    hip_name: Optional[str] = None
    tic_id: Optional[str] = None
    disc_pubdate: Optional[str] = None
    disc_year: Optional[str] = None
    disc_method: Optional[str] = None
    discoverymethod: Optional[str] = None
    disc_locale: Optional[str] = None
    disc_facility: Optional[str] = None
    disc_instrument: Optional[str] = None
    disc_telescope: Optional[str] = None
    disc_refname: Optional[str] = None
    ra: Optional[str] = None
    raerr1: Optional[str] = None
    raerr2: Optional[str] = None
    rasymerr: Optional[str] = None
    rastr: Optional[str] = None
    ra_solnid: Optional[str] = None
    ra_reflink: Optional[str] = None
    dec: Optional[str] = None
    decerr1: Optional[str] = None
    decerr2: Optional[str] = None
    decsymerr: Optional[str] = None
    decstr: Optional[str] = None
    dec_solnid: Optional[str] = None
    dec_reflink: Optional[str] = None
    glon: Optional[str] = None
    glonerr1: Optional[str] = None
    glonerr2: Optional[str] = None
    glonsymerr: Optional[str] = None
    glonstr: Optional[str] = None
    glon_solnid: Optional[str] = None
    glon_reflink: Optional[str] = None
    glat: Optional[str] = None
    glaterr1: Optional[str] = None
    glaterr2: Optional[str] = None
    glatsymerr: Optional[str] = None
    glatstr: Optional[str] = None
    glat_solnid: Optional[str] = None
    glat_reflink: Optional[str] = None
    elon: Optional[str] = None
    elonerr1: Optional[str] = None
    elonerr2: Optional[str] = None
    elonsymerr: Optional[str] = None
    elonstr: Optional[str] = None
    elon_solnid: Optional[str] = None
    elon_reflink: Optional[str] = None
    elat: Optional[str] = None
    elaterr1: Optional[str] = None
    elaterr2: Optional[str] = None
    elatsymerr: Optional[str] = None
    elat_solnid: Optional[str] = None
    elat_reflink: Optional[str] = None
    elatstr: Optional[str] = None
    pl_orbper: Optional[str] = None
    pl_orbpererr1: Optional[str] = None
    pl_orbpererr2: Optional[str] = None
    pl_orbpersymerr: Optional[str] = None
    pl_orbperlim: Optional[str] = None
    pl_orbperstr: Optional[str] = None
    pl_orbperformat: Optional[str] = None
    pl_orbper_solnid: Optional[str] = None
    pl_orbper_reflink: Optional[str] = None
    pl_orblpererr1: Optional[str] = None
    pl_orblper: Optional[str] = None
    pl_orblpererr2: Optional[str] = None
    pl_orblpersymerr: Optional[str] = None
    pl_orblperlim: Optional[str] = None
    pl_orblperstr: Optional[str] = None
    pl_orblperformat: Optional[str] = None
    pl_orblper_solnid: Optional[str] = None
    pl_orblper_reflink: Optional[str] = None
    pl_orbsmax: Optional[str] = None
    pl_orbsmaxerr1: Optional[str] = None
    pl_orbsmaxerr2: Optional[str] = None
    pl_orbsmaxsymerr: Optional[str] = None
    pl_orbsmaxlim: Optional[str] = None
    pl_orbsmaxstr: Optional[str] = None
    pl_orbsmaxformat: Optional[str] = None
    pl_orbsmax_solnid: Optional[str] = None
    pl_orbsmax_reflink: Optional[str] = None
    pl_orbincl: Optional[str] = None
    pl_orbinclerr1: Optional[str] = None
    pl_orbinclerr2: Optional[str] = None
    pl_orbinclsymerr: Optional[str] = None
    pl_orbincllim: Optional[str] = None
    pl_orbinclstr: Optional[str] = None
    pl_orbinclformat: Optional[str] = None
    pl_orbincl_solnid: Optional[str] = None
    pl_orbincl_reflink: Optional[str] = None
    pl_orbtper: Optional[str] = None
    pl_orbtpererr1: Optional[str] = None
    pl_orbtpererr2: Optional[str] = None
    pl_orbtpersymerr: Optional[str] = None
    pl_orbtperlim: Optional[str] = None
    pl_orbtperstr: Optional[str] = None
    pl_orbtperformat: Optional[str] = None
    pl_orbtper_solnid: Optional[str] = None
    pl_orbtper_reflink: Optional[str] = None
    pl_orbeccen: Optional[str] = None
    pl_orbeccenerr1: Optional[str] = None
    pl_orbeccenerr2: Optional[str] = None
    pl_orbeccensymerr: Optional[str] = None
    pl_orbeccenlim: Optional[str] = None
    pl_orbeccenstr: Optional[str] = None
    pl_orbeccenformat: Optional[str] = None
    pl_orbeccen_solnid: Optional[str] = None
    pl_orbeccen_reflink: Optional[str] = None
    pl_eqt: Optional[str] = None
    pl_eqterr1: Optional[str] = None
    pl_eqterr2: Optional[str] = None
    pl_eqtsymerr: Optional[str] = None
    pl_eqtlim: Optional[str] = None
    pl_eqtstr: Optional[str] = None
    pl_eqtformat: Optional[str] = None
    pl_eqt_solnid: Optional[str] = None
    pl_eqt_reflink: Optional[str] = None
    pl_occdep: Optional[str] = None
    pl_occdeperr1: Optional[str] = None
    pl_occdeperr2: Optional[str] = None
    pl_occdepsymerr: Optional[str] = None
    pl_occdeplim: Optional[str] = None
    pl_occdepstr: Optional[str] = None
    pl_occdepformat: Optional[str] = None
    pl_occdep_solnid: Optional[str] = None
    pl_occdep_reflink: Optional[str] = None
    pl_insol: Optional[str] = None
    pl_insolerr1: Optional[str] = None
    pl_insolerr2: Optional[str] = None
    pl_insolsymerr: Optional[str] = None
    pl_insollim: Optional[str] = None
    pl_insolstr: Optional[str] = None
    pl_insolformat: Optional[str] = None
    pl_insol_solnid: Optional[str] = None
    pl_insol_reflink: Optional[str] = None
    pl_dens: Optional[str] = None
    pl_denserr1: Optional[str] = None
    sy_umagerr1: Optional[str] = None
    sy_umagerr2: Optional[str] = None
    sy_umaglim: Optional[str] = None
    sy_umagsymerr: Optional[str] = None
    sy_umagstr: Optional[str] = None
    sy_umagformat: Optional[str] = None
    sy_umag_solnid: Optional[str] = None
    sy_umag_reflink: Optional[str] = None
    sy_rmag: Optional[str] = None
    sy_rmagerr1: Optional[str] = None
    sy_rmagerr2: Optional[str] = None
    sy_rmaglim: Optional[str] = None
    sy_rmagsymerr: Optional[str] = None
    sy_rmagstr: Optional[str] = None
    sy_rmagformat: Optional[str] = None
    sy_rmag_solnid: Optional[str] = None
    sy_rmag_reflink: Optional[str] = None
    sy_imag: Optional[str] = None
    sy_imagerr1: Optional[str] = None
    sy_imagerr2: Optional[str] = None
    sy_imaglim: Optional[str] = None
    sy_imagsymerr: Optional[str] = None
    sy_imagstr: Optional[str] = None
    sy_imagformat: Optional[str] = None
    sy_imag_solnid: Optional[str] = None
    sy_imag_reflink: Optional[str] = None
    sy_zmag: Optional[str] = None
    sy_zmagerr1: Optional[str] = None
    sy_zmagerr2: Optional[str] = None
    sy_zmaglim: Optional[str] = None
    sy_zmagsymerr: Optional[str] = None
    sy_zmagstr: Optional[str] = None
    sy_zmagformat: Optional[str] = None
    sy_zmag_solnid: Optional[str] = None
    sy_zmag_reflink: Optional[str] = None
    sy_w1mag: Optional[str] = None
    sy_w1magerr1: Optional[str] = None
    sy_w1magerr2: Optional[str] = None
    sy_w1maglim: Optional[str] = None
    sy_w1magsymerr: Optional[str] = None
    sy_w1magstr: Optional[str] = None
    sy_w1magformat: Optional[str] = None
    sy_w1mag_solnid: Optional[str] = None
    sy_w1mag_reflink: Optional[str] = None
    sy_w2mag: Optional[str] = None
    sy_w2magerr1: Optional[str] = None
    sy_w2magerr2: Optional[str] = None
    sy_w2maglim: Optional[str] = None
    sy_w2magsymerr: Optional[str] = None
    sy_w2magstr: Optional[str] = None
    sy_w2magformat: Optional[str] = None
    sy_w2mag_solnid: Optional[str] = None
    sy_w2mag_reflink: Optional[str] = None
    sy_w3mag: Optional[str] = None
    sy_w3magerr1: Optional[str] = None
    sy_w3magerr2: Optional[str] = None
    sy_w3maglim: Optional[str] = None
    sy_w3magsymerr: Optional[str] = None
    sy_w3magstr: Optional[str] = None
    sy_w3magformat: Optional[str] = None
    sy_w3mag_solnid: Optional[str] = None
    sy_w3mag_reflink: Optional[str] = None
    sy_w4mag: Optional[str] = None
    sy_w4magerr1: Optional[str] = None
    sy_w4magerr2: Optional[str] = None
    sy_w4maglim: Optional[str] = None
    sy_w4magsymerr: Optional[str] = None
    sy_w4magstr: Optional[str] = None
    sy_w4magformat: Optional[str] = None
    sy_w4mag_solnid: Optional[str] = None
    sy_w4mag_reflink: Optional[str] = None
    sy_gmag: Optional[str] = None
    sy_gmagerr1: Optional[str] = None
    sy_gmagerr2: Optional[str] = None
    sy_gmaglim: Optional[str] = None
    sy_gmagsymerr: Optional[str] = None
    sy_gmagstr: Optional[str] = None
    sy_gmagformat: Optional[str] = None
    sy_gmag_solnid: Optional[str] = None
    sy_gmag_reflink: Optional[str] = None
    sy_gaiamag: Optional[str] = None
    sy_gaiamagerr1: Optional[str] = None
    sy_gaiamagerr2: Optional[str] = None
    sy_gaiamaglim: Optional[str] = None
    sy_gaiamagsymerr: Optional[str] = None
    sy_gaiamagstr: Optional[str] = None
    sy_gaiamagformat: Optional[str] = None
    sy_gaiamag_solnid: Optional[str] = None
    sy_gaiamag_reflink: Optional[str] = None
    sy_tmag: Optional[str] = None
    sy_tmagerr1: Optional[str] = None
    sy_tmagerr2: Optional[str] = None
    sy_tmaglim: Optional[str] = None
    sy_tmagsymerr: Optional[str] = None
    sy_tmagstr: Optional[str] = None
    sy_tmagformat: Optional[str] = None
    sy_tmag_solnid: Optional[str] = None
    sy_tmag_reflink: Optional[str] = None
    sy_name: Optional[str] = None
    pl_controv_flag: Optional[str] = None
    pl_orbtper_systemref: Optional[str] = None
    pl_tranmid_systemref: Optional[str] = None
    st_metratio: Optional[str] = None
    st_spectype: Optional[str] = None
    st_spectype_solnid: Optional[str] = None
    st_spectype_reflink: Optional[str] = None
    sy_plxlim: Optional[str] = None
    sy_kepmag: Optional[str] = None
    sy_kepmagerr1: Optional[str] = None
    sy_kepmagerr2: Optional[str] = None
    sy_kepmaglim: Optional[str] = None
    sy_kepmagsymerr: Optional[str] = None
    sy_kepmagstr: Optional[str] = None
    sy_kepformat: Optional[str] = None
    sy_kepmag_solnid: Optional[str] = None
    sy_kepmag_reflink: Optional[str] = None
    st_rotp: Optional[str] = None
    st_rotperr1: Optional[str] = None
    st_rotperr2: Optional[str] = None
    st_rotpsymerr: Optional[str] = None
    st_rotplim: Optional[str] = None
    st_rotpstr: Optional[str] = None
    st_rotpformat: Optional[str] = None
    st_rotp_solnid: Optional[str] = None
    st_rotp_reflink: Optional[str] = None
    pl_projobliq: Optional[str] = None
    pl_projobliqerr1: Optional[str] = None
    pl_projobliqerr2: Optional[str] = None
    pl_projobliqsymerr: Optional[str] = None
    pl_projobliqlim: Optional[str] = None
    pl_projobliqstr: Optional[str] = None
    pl_projobliqformat: Optional[str] = None
    pl_denserr2: Optional[str] = None
    pl_denssymerr: Optional[str] = None
    pl_denslim: Optional[str] = None
    pl_densstr: Optional[str] = None
    pl_densformat: Optional[str] = None
    pl_dens_solnid: Optional[str] = None
    pl_dens_reflink: Optional[str] = None
    pl_trandep: Optional[str] = None
    pl_trandeperr1: Optional[str] = None
    pl_trandeperr2: Optional[str] = None
    pl_trandepsymerr: Optional[str] = None
    pl_trandeplim: Optional[str] = None
    pl_trandepstr: Optional[str] = None
    pl_trandepformat: Optional[str] = None
    pl_trandep_solnid: Optional[str] = None
    pl_trandep_reflink: Optional[str] = None
    pl_tranmid: Optional[str] = None
    pl_tranmiderr1: Optional[str] = None
    pl_tranmiderr2: Optional[str] = None
    pl_tranmidsymerr: Optional[str] = None
    pl_tranmidlim: Optional[str] = None
    pl_tranmidstr: Optional[str] = None
    pl_tranmidformat: Optional[str] = None
    pl_tranmid_solnid: Optional[str] = None
    pl_tranmid_reflink: Optional[str] = None
    pl_trandur: Optional[str] = None
    pl_trandurerr1: Optional[str] = None
    pl_trandurerr2: Optional[str] = None
    pl_trandursymerr: Optional[str] = None
    pl_trandurlim: Optional[str] = None
    pl_trandurstr: Optional[str] = None
    pl_trandurformat: Optional[str] = None
    pl_trandur_solnid: Optional[str] = None
    pl_trandur_reflink: Optional[str] = None
    pl_rvamp: Optional[str] = None
    pl_rvamperr1: Optional[str] = None
    pl_rvamperr2: Optional[str] = None
    pl_rvampsymerr: Optional[str] = None
    pl_rvamplim: Optional[str] = None
    pl_rvampstr: Optional[str] = None
    pl_rvampformat: Optional[str] = None
    pl_rvamp_solnid: Optional[str] = None
    pl_rvamp_reflink: Optional[str] = None
    pl_radj: Optional[str] = None
    pl_radjerr1: Optional[str] = None
    pl_radjerr2: Optional[str] = None
    pl_radjsymerr: Optional[str] = None
    pl_radjlim: Optional[str] = None
    pl_radjstr: Optional[str] = None
    pl_radjformat: Optional[str] = None
    pl_radj_solnid: Optional[str] = None
    pl_radj_reflink: Optional[str] = None
    pl_rade: Optional[str] = None
    pl_radeerr1: Optional[str] = None
    pl_radeerr2: Optional[str] = None
    pl_radesymerr: Optional[str] = None
    pl_radelim: Optional[str] = None
    pl_radestr: Optional[str] = None
    pl_radeformat: Optional[str] = None
    pl_rade_solnid: Optional[str] = None
    pl_rade_reflink: Optional[str] = None
    pl_ratror: Optional[str] = None
    pl_ratrorerr1: Optional[str] = None
    pl_ratrorerr2: Optional[str] = None
    pl_ratrorsymerr: Optional[str] = None
    pl_ratrorlim: Optional[str] = None
    pl_ratrorstr: Optional[str] = None
    pl_ratrorformat: Optional[str] = None
    pl_ratror_solnid: Optional[str] = None
    pl_ratror_reflink: Optional[str] = None
    pl_ratdor: Optional[str] = None
    pl_trueobliq: Optional[str] = None
    pl_trueobliqerr1: Optional[str] = None
    pl_trueobliqerr2: Optional[str] = None
    pl_trueobliqsymerr: Optional[str] = None
    pl_trueobliqlim: Optional[str] = None
    pl_trueobliqstr: Optional[str] = None
    pl_trueobliqformat: Optional[str] = None
    pl_trueobliq_solnid: Optional[str] = None
    pl_trueobliq_reflink: Optional[str] = None
    st_log_rhk: Optional[str] = None
    st_log_rhkerr1: Optional[str] = None
    st_log_rhkerr2: Optional[str] = None
    st_log_rhksymerr: Optional[str] = None
    st_log_rhklim: Optional[str] = None
    st_log_rhkstr: Optional[str] = None
    st_log_rhkformat: Optional[str] = None
    st_log_rhk_solnid: Optional[str] = None
    st_log_rhk_reflink: Optional[str] = None
    st_metn: Optional[str] = None
    sy_icmag: Optional[str] = None
    sy_icmagerr1: Optional[str] = None
    sy_icmagerr2: Optional[str] = None
    sy_icmagsymerr: Optional[str] = None
    sy_icmagstr: Optional[str] = None
    sy_icmagformat: Optional[str] = None
    sy_icmag_solnid: Optional[str] = None
    sy_icmag_reflink: Optional[str] = None
    pl_pubdate: Optional[str] = None
    dkin_flag: Optional[str] = None
    pl_ratdorerr1: Optional[str] = None
    pl_ratdorerr2: Optional[str] = None
    pl_ratdorsymerr: Optional[str] = None
    pl_ratdorlim: Optional[str] = None
    pl_ratdorstr: Optional[str] = None
    pl_ratdorformat: Optional[str] = None
    pl_ratdor_solnid: Optional[str] = None
    pl_ratdor_reflink: Optional[str] = None
    pl_imppar: Optional[str] = None
    pl_impparerr1: Optional[str] = None
    pl_impparerr2: Optional[str] = None
    pl_impparsymerr: Optional[str] = None
    pl_impparlim: Optional[str] = None
    pl_impparstr: Optional[str] = None
    pl_impparformat: Optional[str] = None
    pl_imppar_solnid: Optional[str] = None
    pl_imppar_reflink: Optional[str] = None
    pl_cmassj: Optional[str] = None
    pl_cmassjerr1: Optional[str] = None
    pl_cmassjerr2: Optional[str] = None
    pl_cmassjsymerr: Optional[str] = None
    pl_cmassjlim: Optional[str] = None
    pl_cmassjstr: Optional[str] = None
    pl_cmassjformat: Optional[str] = None
    pl_cmassj_solnid: Optional[str] = None
    pl_cmassj_reflink: Optional[str] = None
    pl_cmasse: Optional[str] = None
    pl_cmasseerr1: Optional[str] = None
    pl_cmasseerr2: Optional[str] = None
    pl_cmassesymerr: Optional[str] = None
    pl_cmasselim: Optional[str] = None
    pl_cmassestr: Optional[str] = None
    pl_cmasseformat: Optional[str] = None
    pl_cmasse_solnid: Optional[str] = None
    pl_cmasse_reflink: Optional[str] = None
    pl_massj: Optional[str] = None
    pl_massjerr1: Optional[str] = None
    pl_massjerr2: Optional[str] = None
    pl_massjsymerr: Optional[str] = None
    pl_massjlim: Optional[str] = None
    pl_massjstr: Optional[str] = None
    pl_massjformat: Optional[str] = None
    pl_massj_solnid: Optional[str] = None
    pl_massj_reflink: Optional[str] = None
    pl_masse: Optional[str] = None
    pl_masseerr1: Optional[str] = None
    pl_masseerr2: Optional[str] = None
    pl_massesymerr: Optional[str] = None
    pl_masselim: Optional[str] = None
    pl_massestr: Optional[str] = None
    pl_masseformat: Optional[str] = None
    pl_masse_solnid: Optional[str] = None
    pl_masse_reflink: Optional[str] = None
    pl_bmassj: Optional[str] = None
    pl_bmassjerr1: Optional[str] = None
    pl_bmassjerr2: Optional[str] = None
    pl_bmassjsymerr: Optional[str] = None
    pl_bmassjlim: Optional[str] = None
    pl_bmassjstr: Optional[str] = None
    pl_bmassjformat: Optional[str] = None
    pl_bmassj_solnid: Optional[str] = None
    pl_bmassj_reflink: Optional[str] = None
    pl_bmasse: Optional[str] = None
    pl_bmasseerr1: Optional[str] = None
    pl_bmasseerr2: Optional[str] = None
    pl_bmassesymerr: Optional[str] = None
    pl_bmasselim: Optional[str] = None
    pl_bmassestr: Optional[str] = None
    pl_bmasseformat: Optional[str] = None
    pl_bmasse_solnid: Optional[str] = None
    pl_bmasse_reflink: Optional[str] = None
    pl_bmassprov: Optional[str] = None
    pl_msinij: Optional[str] = None
    pl_msinijerr1: Optional[str] = None
    pl_msinijerr2: Optional[str] = None
    pl_msinijsymerr: Optional[str] = None
    pl_msinijlim: Optional[str] = None
    pl_msinijstr: Optional[str] = None
    pl_msinijformat: Optional[str] = None
    pl_msinij_solnid: Optional[str] = None
    pl_msinij_reflink: Optional[str] = None
    pl_msinie: Optional[str] = None
    pl_msinieerr1: Optional[str] = None
    pl_msinieerr2: Optional[str] = None
    pl_msiniesymerr: Optional[str] = None
    pl_msinielim: Optional[str] = None
    pl_msiniestr: Optional[str] = None
    pl_msinieformat: Optional[str] = None
    pl_msinie_solnid: Optional[str] = None
    pl_msinie_reflink: Optional[str] = None
    st_teff: Optional[str] = None
    st_tefferr1: Optional[str] = None
    st_tefferr2: Optional[str] = None
    st_teffsymerr: Optional[str] = None
    st_tefflim: Optional[str] = None
    st_teffstr: Optional[str] = None
    st_teffformat: Optional[str] = None
    st_teff_solnid: Optional[str] = None
    st_teff_reflink: Optional[str] = None
    st_met: Optional[str] = None
    st_meterr1: Optional[str] = None
    st_meterr2: Optional[str] = None
    st_metsymerr: Optional[str] = None
    st_metlim: Optional[str] = None
    st_metstr: Optional[str] = None
    st_metformat: Optional[str] = None
    st_met_solnid: Optional[str] = None
    st_met_reflink: Optional[str] = None
    st_radv: Optional[str] = None
    st_radverr1: Optional[str] = None
    st_radverr2: Optional[str] = None
    st_radvsymerr: Optional[str] = None
    st_radvlim: Optional[str] = None
    st_radvstr: Optional[str] = None
    st_radvformat: Optional[str] = None
    st_radv_solnid: Optional[str] = None
    st_radv_reflink: Optional[str] = None
    st_vsin: Optional[str] = None
    st_vsinerr1: Optional[str] = None
    st_vsinerr2: Optional[str] = None
    st_vsinsymerr: Optional[str] = None
    st_vsinlim: Optional[str] = None
    st_vsinstr: Optional[str] = None
    st_vsin_solnid: Optional[str] = None
    st_vsin_reflink: Optional[str] = None
    st_vsinformat: Optional[str] = None
    st_lum: Optional[str] = None
    st_lumerr1: Optional[str] = None
    st_lumerr2: Optional[str] = None
    st_lumsymerr: Optional[str] = None
    st_lumlim: Optional[str] = None
    st_lumstr: Optional[str] = None
    st_lumformat: Optional[str] = None
    st_lum_solnid: Optional[str] = None
    st_lum_reflink: Optional[str] = None
    st_logg: Optional[str] = None
    st_loggerr1: Optional[str] = None
    st_loggerr2: Optional[str] = None
    st_loggsymerr: Optional[str] = None
    st_logglim: Optional[str] = None
    st_loggstr: Optional[str] = None
    st_loggformat: Optional[str] = None
    st_logg_solnid: Optional[str] = None
    st_logg_reflink: Optional[str] = None
    st_age: Optional[str] = None
    st_ageerr1: Optional[str] = None
    st_ageerr2: Optional[str] = None
    st_agesymerr: Optional[str] = None
    st_agelim: Optional[str] = None
    st_agestr: Optional[str] = None
    st_ageformat: Optional[str] = None
    st_age_solnid: Optional[str] = None
    st_age_reflink: Optional[str] = None
    st_mass: Optional[str] = None
    st_masserr1: Optional[str] = None
    st_masserr2: Optional[str] = None
    st_masssymerr: Optional[str] = None
    st_masslim: Optional[str] = None
    st_massstr: Optional[str] = None
    st_massformat: Optional[str] = None
    st_mass_solnid: Optional[str] = None
    st_mass_reflink: Optional[str] = None
    st_dens: Optional[str] = None
    st_denserr1: Optional[str] = None
    st_denserr2: Optional[str] = None
    st_denssymerr: Optional[str] = None
    st_denslim: Optional[str] = None
    st_densstr: Optional[str] = None
    st_densformat: Optional[str] = None
    st_dens_solnid: Optional[str] = None
    st_dens_reflink: Optional[str] = None
    st_rad: Optional[str] = None
    st_raderr1: Optional[str] = None
    st_raderr2: Optional[str] = None
    st_radsymerr: Optional[str] = None
    st_radlim: Optional[str] = None
    st_radstr: Optional[str] = None
    st_radformat: Optional[str] = None
    st_rad_solnid: Optional[str] = None
    st_rad_reflink: Optional[str] = None
    systemid: Optional[str] = None
    ttv_flag: Optional[str] = None
    ptv_flag: Optional[str] = None
    tran_flag: Optional[str] = None
    rv_flag: Optional[str] = None
    ast_flag: Optional[str] = None
    obm_flag: Optional[str] = None
    micro_flag: Optional[str] = None
    etv_flag: Optional[str] = None
    ima_flag: Optional[str] = None
    pul_flag: Optional[str] = None
    disc_refid: Optional[str] = None
    sy_snum: Optional[str] = None
    sy_pnum: Optional[str] = None
    sy_mnum: Optional[str] = None
    st_nphot: Optional[str] = None
    st_nrvc: Optional[str] = None
    st_nspec: Optional[str] = None
    pl_nespec: Optional[str] = None
    pl_ntranspec: Optional[str] = None
    pl_nnotes: Optional[str] = None
    sy_pm: Optional[str] = None
    sy_pmerr1: Optional[str] = None
    sy_pmerr2: Optional[str] = None
    sy_pmsymerr: Optional[str] = None
    sy_pmlim: Optional[str] = None
    sy_pmstr: Optional[str] = None
    sy_pmformat: Optional[str] = None
    sy_pm_solnid: Optional[str] = None
    sy_pm_reflink: Optional[str] = None
    sy_pmra: Optional[str] = None
    sy_pmraerr1: Optional[str] = None
    sy_pmraerr2: Optional[str] = None
    sy_pmrasymerr: Optional[str] = None
    sy_pmralim: Optional[str] = None
    sy_pmrastr: Optional[str] = None
    sy_pmraformat: Optional[str] = None
    sy_pmra_solnid: Optional[str] = None
    sy_pmra_reflink: Optional[str] = None
    sy_pmdec: Optional[str] = None
    sy_pmdecerr1: Optional[str] = None
    sy_pmdecerr2: Optional[str] = None
    sy_pmdecsymerr: Optional[str] = None
    sy_pmdeclim: Optional[str] = None
    sy_pmdecstr: Optional[str] = None
    sy_pmdecformat: Optional[str] = None
    sy_pmdec_solnid: Optional[str] = None
    sy_pmdec_reflink: Optional[str] = None
    sy_plx: Optional[str] = None
    sy_plxerr1: Optional[str] = None
    sy_plxerr2: Optional[str] = None
    sy_plxsymerr: Optional[str] = None
    sy_plxstr: Optional[str] = None
    sy_plxformat: Optional[str] = None
    sy_plx_solnid: Optional[str] = None
    sy_plx_reflink: Optional[str] = None
    sy_dist: Optional[str] = None
    sy_disterr1: Optional[str] = None
    sy_disterr2: Optional[str] = None
    sy_distsymerr: Optional[str] = None
    sy_distlim: Optional[str] = None
    sy_diststr: Optional[str] = None
    sy_distformat: Optional[str] = None
    sy_dist_solnid: Optional[str] = None
    sy_dist_reflink: Optional[str] = None
    sy_bmag: Optional[str] = None
    sy_bmagerr1: Optional[str] = None
    sy_bmagerr2: Optional[str] = None
    sy_bmaglim: Optional[str] = None
    sy_bmagsymerr: Optional[str] = None
    sy_bmagstr: Optional[str] = None
    sy_bmagformat: Optional[str] = None
    sy_bmag_solnid: Optional[str] = None
    sy_bmag_reflink: Optional[str] = None
    sy_vmag: Optional[str] = None
    sy_vmagerr1: Optional[str] = None
    sy_vmagerr2: Optional[str] = None
    sy_vmaglim: Optional[str] = None
    sy_vmagsymerr: Optional[str] = None
    sy_vmagstr: Optional[str] = None
    sy_vmagformat: Optional[str] = None
    sy_vmag_solnid: Optional[str] = None
    sy_vmag_reflink: Optional[str] = None
    sy_jmag: Optional[str] = None
    sy_jmagerr1: Optional[str] = None
    sy_jmagerr2: Optional[str] = None
    sy_jmaglim: Optional[str] = None
    sy_jmagsymerr: Optional[str] = None
    sy_jmagstr: Optional[str] = None
    sy_jmagformat: Optional[str] = None
    sy_jmag_solnid: Optional[str] = None
    sy_jmag_reflink: Optional[str] = None
    sy_hmag: Optional[str] = None
    sy_hmagerr1: Optional[str] = None
    sy_hmagerr2: Optional[str] = None
    sy_hmaglim: Optional[str] = None
    sy_hmagsymerr: Optional[str] = None
    sy_hmagstr: Optional[str] = None
    sy_hmagformat: Optional[str] = None
    sy_hmag_solnid: Optional[str] = None
    sy_hmag_reflink: Optional[str] = None
    sy_kmag: Optional[str] = None
    sy_kmagerr1: Optional[str] = None
    sy_kmagerr2: Optional[str] = None
    sy_kmaglim: Optional[str] = None
    sy_kmagsymerr: Optional[str] = None
    sy_kmagstr: Optional[str] = None
    sy_kmagformat: Optional[str] = None
    sy_kmag_solnid: Optional[str] = None
    sy_kmag_reflink: Optional[str] = None
    sy_umag: Optional[str] = None
    pl_projobliq_solnid: Optional[str] = None
    pl_projobliq_reflink: Optional[str] = None
    x: Optional[str] = None
    y: Optional[str] = None
    z: Optional[str] = None
    htm20: Optional[str] = None
    gaia_id: Optional[str] = None
    cb_flag: Optional[str] = None
    pl_angsep: Optional[str] = None
    pl_angseperr1: Optional[str] = None
    pl_angseperr2: Optional[str] = None
    pl_angseplim: Optional[str] = None
    pl_angsepformat: Optional[str] = None
    pl_angsepstr: Optional[str] = None
    pl_angsepsymerr: Optional[str] = None
    pl_angsep_reflink: Optional[str] = None
    pl_ndispec: Optional[str] = None


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
