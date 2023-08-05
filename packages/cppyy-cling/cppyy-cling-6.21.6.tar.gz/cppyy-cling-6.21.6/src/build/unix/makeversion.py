# Script to update base/inc/RVersion.h.
# Called by main Makefile as soon as build/version_number has been updated.
#
# Author: Axel, 2020-03-06

import os, subprocess, re
from datetime import date, datetime

versionline = ""
with open("build/version_number", "r") as file:
  versionline = file.read().replace('\n', '')

matches = re.match(r'^(\d+)[.](\d+)/(\d+)$', versionline).groups()
if len(matches) != 3:
  raise RuntimeError("build/version_number: invalid syntax")

major = int(matches[0])
minor = int(matches[1])
patch = int(matches[2])
vers_code = (major << 16) + (minor << 8) + patch

datenow = date.today().strftime("%b %d %Y") # Sep 11 2019
timenow = datetime.now().strftime("%H:%M:%S") # 15:05:55

sourcecode = """#ifndef ROOT_RVersion
#define ROOT_RVersion

/* Version information automatically generated by installer. */

/*
 * These macros can be used in the following way:
 *
 *    #if ROOT_VERSION_CODE >= ROOT_VERSION(6,32,4)
 *       #include <newheader.h>
 *    #else
 *       #include <oldheader.h>
 *    #endif
 *
*/

#define ROOT_RELEASE "{}"
#define ROOT_RELEASE_DATE "{}"
#define ROOT_RELEASE_TIME "{}"
#define ROOT_VERSION(a,b,c) (((a) << 16) + ((b) << 8) + (c))
#define ROOT_VERSION_CODE ROOT_VERSION({},{},{}) /* {} */

#endif
""".format(versionline, datenow, timenow, major, minor, patch, vers_code)

with open('core/base/inc/RVersion.h', 'w') as file:
  file.write(sourcecode)

subprocess.check_call("build/unix/coreteam.sh rootx/src/rootcoreteam.h", shell = True)

print("Committing changes.")
subprocess.check_call(['git', 'commit',
  'core/base/inc/RVersion.h', 'rootx/src/rootcoreteam.h',
  'build/version_number', 'documentation/doxygen/Doxyfile',
  '-m', '"Update ROOT version files to v{}."'.format(versionline)])

print("""
New version is {}.
See https://root.cern/release-checklist for the next steps,
for instance tagging if this is a release.""".format(versionline))
