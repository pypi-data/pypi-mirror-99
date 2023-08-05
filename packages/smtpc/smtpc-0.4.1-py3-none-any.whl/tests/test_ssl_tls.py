import pytest


@pytest.mark.parametrize(
    "port_cli,ssl_cli,tls_cli,no_ssl_cli,no_tls_cli,"
    "port_profile,ssl_profile,tls_profile,no_ssl_profile,no_tls_profile,"
    "expected_ssl,expected_tls",
    [
        # port  ssl    tls    no_ssl  no_tls  port   ssl    tls    no_ssl  no_tls  ssl     tls
        [ 123,  None,  None,  None,   None,   None,  None,  None,  None,   None,   False,  False ],
        [ 25,   None,  None,  None,   None,   None,  None,  None,  None,   None,   False,  False ],
        [ 465,  None,  None,  None,   None,   None,  None,  None,  None,   None,   True,   False ],
        [ 587,  None,  None,  None,   None,   None,  None,  None,  None,   None,   False,  True ],

        [ 123,  True,  None,  None,   None,   None,  None,  None,  None,   None,   True,   False ],
        [ 25,   True,  None,  None,   None,   None,  None,  None,  None,   None,   True,   False ],
        [ 465,  True,  None,  None,   None,   None,  None,  None,  None,   None,   True,   False ],
        [ 587,  True,  None,  None,   None,   None,  None,  None,  None,   None,   True,   False ],

        [ 123,  None,  True,  None,   None,   None,  None,  None,  None,   None,   False,  True ],
        [ 25,   None,  True,  None,   None,   None,  None,  None,  None,   None,   False,  True ],
        [ 465,  None,  True,  None,   None,   None,  None,  None,  None,   None,   False,  True ],
        [ 587,  None,  True,  None,   None,   None,  None,  None,  None,   None,   False,  True ],

        [ 123,  None,  None,  True,   None,   None,  None,  None,  None,   None,   False,  False ],
        [ 25,   None,  None,  True,   None,   None,  None,  None,  None,   None,   False,  False ],
        [ 465,  None,  None,  True,   None,   None,  None,  None,  None,   None,   False,  False ],
        [ 587,  None,  None,  True,   None,   None,  None,  None,  None,   None,   False,  True ],

        # port  ssl    tls    no_ssl  no_tls  port   ssl    tls    no_ssl  no_tls  ssl     tls
        [ 123,  None,  None,  None,   True,   None,  None,  None,  None,   None,   False,  False ],
        [ 25,   None,  None,  None,   True,   None,  None,  None,  None,   None,   False,  False ],
        [ 465,  None,  None,  None,   True,   None,  None,  None,  None,   None,   True,   False ],
        [ 587,  None,  None,  None,   True,   None,  None,  None,  None,   None,   False,  False ],

        [ 123,  None,  None,  None,   None,   None,  True,  None,  None,   None,   True,   False ],
        [ 25,   None,  None,  None,   None,   None,  True,  None,  None,   None,   True,   False ],
        [ 465,  None,  None,  None,   None,   None,  True,  None,  None,   None,   True,   False ],
        [ 587,  None,  None,  None,   None,   None,  True,  None,  None,   None,   True,   False ],

        [ 123,  None,  None,  None,   None,   None,  None,  True,  None,   None,   False,  True ],
        [ 25,   None,  None,  None,   None,   None,  None,  True,  None,   None,   False,  True ],
        [ 465,  None,  None,  None,   None,   None,  None,  True,  None,   None,   False,  True ],
        [ 587,  None,  None,  None,   None,   None,  None,  True,  None,   None,   False,  True ],

        [ 123,  None,  None,  None,   None,   None,  None,  None,  True,   None,   False,  False ],
        [ 25,   None,  None,  None,   None,   None,  None,  None,  True,   None,   False,  False ],
        [ 465,  None,  None,  None,   None,   None,  None,  None,  True,   None,   False,  False ],
        [ 587,  None,  None,  None,   None,   None,  None,  None,  True,   None,   False,  True ],

        # port  ssl    tls    no_ssl  no_tls  port   ssl    tls    no_ssl  no_tls  ssl     tls
        [ 123,  None,  None,  None,   None,   None,  None,  None,  None,   True,   False,  False ],
        [ 25,   None,  None,  None,   None,   None,  None,  None,  None,   True,   False,  False ],
        [ 465,  None,  None,  None,   None,   None,  None,  None,  None,   True,   True,   False ],
        [ 587,  None,  None,  None,   None,   None,  None,  None,  None,   True,   False,  False ],

        [ 123,  None,  None,  None,   None,   None,  None,  None,  None,   True,   False,  False ],
        [ 25,   None,  None,  None,   None,   None,  None,  None,  None,   True,   False,  False ],
        [ 465,  None,  None,  None,   None,   None,  None,  None,  None,   True,   True,   False ],
        [ 587,  None,  None,  None,   None,   None,  None,  None,  None,   True,   False,  False ],

    ]
)
def test_ssl_tls(
    port_cli, ssl_cli, tls_cli, no_ssl_cli, no_tls_cli,
    port_profile, ssl_profile, tls_profile, no_ssl_profile, no_tls_profile,
    expected_ssl, expected_tls
):
    pass
