import os, sys, shutil

###############################################
destination = '/home/kandasamyk/g_files/'
# Note: The destination directory must already exist.
shot = 163303
runid = '2001'
# Note: For runid, use numbers instead of letters,
#       e.g. '0102' instead of 'A02', '2001' instead of 'T01', etc.
runid_full = str(shot) + runid
geq_extract_times = range(500, 3250, 250)
###############################################


# Load TRANSP
transp = OMFIT.loadModule('TRANSP',"OMFIT['TRANSP']")

# Load TRXPL and run it once
trxpl = OMFIT.loadModule('TRXPL',"OMFIT['TRXPL']")
trxpl['SETTINGS']['EXPERIMENT']['time'] = geq_extract_times[0]
transp['SETTINGS']['EXPERIMENT']['time'] = geq_extract_times[0]
transp['TRXPL']['SCRIPTS']['trxpl'].run()

# Extract multiple g-files in parallel.
sims={}
sims[0]={'runid':(runid_full), 'time':geq_extract_times}
OMFIT['TRANSP']['TRXPL']['SCRIPTS']['multi'].run(sims=sims)

def get_geq_filename(time):
  eq_name = 'D3D_%s_%d' % (runid_full, time)
  return OMFIT['TRANSP']['TRXPL']['MULTI'][eq_name]['gEQDSK'].filename

# Copy the g-files to destination
for time in geq_extract_times:
  original_file = get_geq_filename(time)
  new_file = '%s%s_%d.geq' % (destination, runid_full, time)
  shutil.copy(original_file, new_file)

print 'Extracted GEQ files to %s' % (destination)
