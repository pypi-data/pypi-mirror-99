"""
Instantiate a delayed snowmobile.Snowmobile object and inspect configuration model.
../docs/snippets/configuration/inspect_configuration.py
"""
import snowmobile

sn = snowmobile.Snowmobile(delay=True)

type(sn.cfg)              #> snowmobile.core.configuration.Configuration
print(sn.cfg.location)    #  'path/to/your/snowmobile.toml'

type(sn.cfg.connection)   #> snowmobile.core.cfg.connection.Connection
type(sn.cfg.loading)      #> snowmobile.core.cfg.loading.Loading
type(sn.cfg.script)       #> snowmobile.core.cfg.script.Script
type(sn.cfg.sql)          #> snowmobile.core.cfg.other.SQL
type(sn.cfg.ext_sources)  #> snowmobile.core.cfg.other.Location

# -- complete example; should run 'as is' --
# snowmobile-include
