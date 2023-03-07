{
    'name': 'KSP Tabungan',
    'version': '16.0.0.1',
    'summary': 'Fitur tabungan',
    'description': 'Fitur tabungan',
    'author': 'Khoerurrizal',
    'website': 'http://khoer.vercel.app',
    'depends': [
        'base'
    ],
    'data': [
        'views/tabungan_view.xml',
        'views/nasabah_view.xml',
        'wizard/wizard_setoran_tabungan_view.xml',
        'wizard/wizard_penarikan_tabungan_view.xml',
        'views/ksp_tabungan_line_type_view.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/ksp.tabungan.line.type.csv',
        'data/config.xml',
        'views/ksp_config_tabungan_view.xml',
        'data/cron.xml'
    ],
    'installable': True,
    'auto_install': False,
}