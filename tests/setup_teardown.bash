# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Henri  GEIST

# This is a common file only meant to be included in a dedicated test suit.

setup_file () {
    bats_require_minimum_version 1.5.0
}


setup () {
    load '/usr/lib/bats/bats-support/load'
    load '/usr/lib/bats/bats-assert/load'
}
