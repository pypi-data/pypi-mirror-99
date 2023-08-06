"""
Styles that can be used in the rectable representations
"""

styles = dict()

styles['rst-grid'] = {'art': [
                   ['+-', '-', '-+-', '-+'],
                   ['| ', '.', ' | ', ' |'],
                   ['+=', '=', '=+=', '=+'],
                   ['| ', '.', ' | ', ' |'],
                   ['+-', '-', '-+-', '-+'],
                   ['+-', '-', '-+-', '-+']],
                      'hhaligns': 'l'}

styles['rst-simple'] = {'art': [
                   ['', '=', ' ', ''],
                   ['', '.', ' ', ''],
                   ['', '=', ' ', ''],
                   ['', '.', ' ', ''],
                    None,
                   ['', '=', ' ', '']],
                       'hhaligns': 'l'}

styles['markdown'] = {'art': [
                    None,
                   ['| ', '.', ' | ', ' |'],
                   ['|-', '-', '-|-', '-|'],
                   ['| ', '.', ' | ', ' |'],
                    None,
                    None],
                      'hhaligns' : 'l'}

styles['jira'] = {'art': [
                    None,
                   ['||', '.', '||', '||'],
                    None,
                   ['| ', '.', '| ', ' |'],
                    None,
                    None],
                  'hhaligns': 'l'}

styles['pretty'] = {'art': [
                   ['+-', '-', '-+-', '-+'],
                   ['| ', '.', ' | ', ' |'],
                   ['+-', '-', '-+-', '-+'],
                   ['| ', '.', ' | ', ' |'],
                    None,
                   ['+-', '-', '-+-', '-+']],
                    'hhaligns': 'c'}

styles['pandas'] = {'art': [
                    None,
                   ['', '.', ' ', ''],
                    None,
                   ['', '.', ' ', ''],
                    None,
                    None],
                    'hhaligns': 'r'}

styles['cmd-history'] = {'art': [
                   ['#-', '-', '-#-', '-#'],
                   ['# ', '.', ' # ', ' #'],
                   ['#=', '=', '=#=', '=#'],
                   ['  ', '.', ' # ', '  '],
                   ['#-', '-', '-#-', '-#'],
                   ['#-', '-', '-#-', '-#']],
                      'hhaligns': 'l'}

styles['html'] = {'art': [
                    None,
                   ['<tr><th>', '.', '</th><th>', '</th></tr>'],
                    None,
                   ['<tr><td>', '.', '</td><td>', '</td></tr>'],
                    None,
                    None],
                  'hhaligns': 'c'}
