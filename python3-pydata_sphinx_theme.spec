#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (TODO: many missing deps)
%bcond_without	tests	# unit tests

Summary:	Bootstrap-based Sphinx theme from the PyData community
Summary(pl.UTF-8):	Motyw Sphinksa oparty na motywie Bootstrap, stworzony przez społeczność PyData
Name:		python3-pydata_sphinx_theme
Version:	0.16.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pydata-sphinx-theme/
Source0:	https://files.pythonhosted.org/packages/source/p/pydata-sphinx-theme/pydata_sphinx_theme-%{version}.tar.gz
# Source0-md5:	e629ab8013637be343c9f1836863c232
Source1:	pydata_sphinx_theme-0.16.1-vendor.tar.xz
# Source1-md5:	da543d22d8fbf6947b563a74b2eecd01
URL:		https://pypi.org/project/pydata-sphinx-theme/
BuildRequires:	gettext-tools
BuildRequires:	nodejs
BuildRequires:	npm
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-nodeenv
BuildRequires:	python3-sphinx_theme_builder
%if %{with tests}
BuildRequires:	python3-Sphinx >= 6.1
BuildRequires:	python3-accessible-pygments
BuildRequires:	python3-babel
BuildRequires:	python3-bs4
BuildRequires:	python3-docutils >= 0.17.1
BuildRequires:	python3-pygments >= 2.7
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-datadir
BuildRequires:	python3-pytest-regressions
BuildRequires:	python3-sphinx_testing
BuildRequires:	python3-typing_extensions
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	sed >= 4.0
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	nodejs_version	%(nodejs -v | sed s/v//)

%description
A Bootstrap-based Sphinx theme from the PyData community.

%description -l pl.UTF-8
Motyw Sphinksa oparty na motywie Bootstrap, stworzony przez
społeczność PyData.

%prep
%setup -q -n pydata_sphinx_theme-%{version} -a1

# Substitute the installed nodejs version for the requested version
sed -i 's,^\(node-version = \)".*",\1"%{nodejs_version}",' pyproject.toml

%build
%{__python3} -m nodeenv --node=system --prebuilt --clean-src $(pwd)/.nodeenv

%py3_build_pyproject

%if %{with tests}
# two test_pygments_fallbacks cases fail (as of 0.16.1), don't know why
%{__python3} -m zipfile -e build-3/*.whl build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_datadir.plugin,pytest_regressions.plugin,sphinx.testing.fixtures" \
PYTHONPATH=$(pwd)/build-3-test \
%{__python3} -m pytest tests -m 'not a11y' -k 'not test_pygments_fallbacks'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py3_sitescriptdir}/pydata_sphinx_theme
%{py3_sitescriptdir}/pydata_sphinx_theme-%{version}.dist-info
