{
    'name': 'KSP Keuntungan',
    'version': '16.0.0.1',
    'summary': 'Perhitungan keuntungan dan bagi hasil',
    'description': 'Perhitungan keuntungan dan bagi hasil',
    'depends': [
        'ksp_simpanan',
        'ksp_tabungan'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/keuntungan_view.xml',
        'views/saham_view.xml',
        'views/nasabah_view.xml',
        'views/tabungan_view.xml',
        'views/buy_saham_view.xml',
        'wizard/wizard_generate_saham_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}