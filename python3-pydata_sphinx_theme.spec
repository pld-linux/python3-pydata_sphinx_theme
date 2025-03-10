#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Bootstrap-based Sphinx theme from the PyData community
Summary(pl.UTF-8):	Motyw Sphinksa oparty na motywie Bootstrap, stworzony przez społeczność PyData
Name:		python3-pydata_sphinx_theme
# versions >= 0.8 require sphinx-theme-builder, which is not ready in PLD
Version:	0.7.2
Release:	3
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pydata-sphinx-theme/
Source0:	https://files.pythonhosted.org/packages/source/p/pydata-sphinx-theme/pydata-sphinx-theme-%{version}.tar.gz
# Source0-md5:	d13330b18df272bd9f46f42b033f1524
Patch0:		pydata_sphinx_theme-deprecated.patch
URL:		https://pypi.org/project/pydata-sphinx-theme/
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-bs4
BuildRequires:	python3-docutils >= 0.17.1
BuildRequires:	python3-packaging
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-regressions
BuildRequires:	python3-sphinx_testing
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Bootstrap-based Sphinx theme from the PyData community.

%description -l pl.UTF-8
Motyw Sphinksa oparty na motywie Bootstrap, stworzony przez
społeczność PyData.

%prep
%setup -q -n pydata-sphinx-theme-%{version}
%patch -P 0 -p1

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_datadir.plugin,pytest_regressions.plugin,sphinx.testing.fixtures" \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py3_sitescriptdir}/pydata_sphinx_theme
%{py3_sitescriptdir}/pydata_sphinx_theme-%{version}-py*.egg-info
