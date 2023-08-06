EAPI=7
PV="5"
DESCRIPTION="Ebuild that assigns read-only variable in global scope"
HOMEPAGE="https://github.com/pkgcore/pkgcheck"
SLOT="0"
LICENSE="BSD"

pkg_pretend() {
	# assignments in function scope are ignored
	PV="6"
}
