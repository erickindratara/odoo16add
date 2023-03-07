{
    'name': 'KSP Pendanaan',
    'version': '16.0.0.1',
    'summary': 'Pengajuan pendanaan sampai dengan pembayaran cicilan',
    'description': 'Pengajuan pendanaan sampai dengan pembayaran cicilan',
    'depends': [
        'mail',
        'ksp_tabungan'
    ],
    'data': [
        'data/action.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/pendanaan_view.xml',
        'views/nasabah_view.xml',
        'views/cicilan_view.xml',
        'views/survey_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}