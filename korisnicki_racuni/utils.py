


def detektirajKorisnika(user):
    if user.role == 1:
        redirectUrl = 'opg_nadzorna_ploca'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'kupac_nadzorna_ploca'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
