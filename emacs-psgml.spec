%define	fname	psgml
%define psgmldir %_datadir/emacs/site-lisp/psgml

Summary:	A GNU Emacs major mode for editing SGML documents
name:		emacs-%fname
Version:	1.2.5
Release: 	 %mkrel 8
Requires: 	sgml-common
Requires: 	emacs >= 20.7
License: 	GPL
URL:		http://www.lysator.liu.se/projects/about_psgml.html
Source: 	ftp://ftp.lysator.liu.se/pub/sgml/psgml-%{version}.tar.bz2
Group: 		Editors
Obsoletes:	psgml
Provides:	psgml = %version-%release
Buildroot: 	%_tmppath/%{name}-root
BuildRequires:	emacs-bin

%description
Emacs is an advanced and extensible editor. An Emacs major mode
customizes Emacs for editing particular types of text documents. PSGML
is a major mode for SGML (a markup language) documents.  PSGML
provides several functionalities for editing SGML documents:
indentation according to element nesting depth and identification of
structural errors (but it is not a validating SGML parser); menus and
commands for inserting tags with only the contextually valid tags;
attribute values can be edited in a separate window with information
about types and defaults; structure based editing includes movement
and killing; and also several commands for folding editing.

%prep
%setup -q -n %fname-%version

%build
%configure
make infodir=%{_infodir} psgmldir=%{psgmldir}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{psgmldir},%{_infodir},%{_libdir}/sgml/cdtd}

%makeinstall psgmldir=$RPM_BUILD_ROOT%{psgmldir} lispdir=$RPM_BUILD_ROOT%{psgmldir}

# Why putting source files ??????
#for i in $RPM_BUILD_ROOT%{psgmldir}/*.elc; do 
#  rm -f $i
#  cp `echo $(basename $i) | sed s/elc/el/` $RPM_BUILD_ROOT%{psgmldir}
#done

make install-info infodir=$RPM_BUILD_ROOT%{_infodir}

install -d %buildroot%{_sysconfdir}/emacs/site-start.d
cat << EOF > %buildroot%{_sysconfdir}/emacs/site-start.d/%{name}-init.el
(add-to-list 'load-path "%{psgmldir}")

(autoload 'sgml-mode "psgml" "Major mode for editing SGML." t)
(autoload 'xml-mode "psgml" "Major mode for editing XML." t)
(if (not (getenv "SGML_CATALOG_FILES"))
   (defvar sgml-catalog-files '("CATALOG" "catalog" "/etc/sgml/catalog""%{_libdir}/sgml/CATALOG" "%{_libdir}/sgml-tools/dtd/catalog"))
  "*List of catalog entry files.
The files are in the format defined in the SGML Open Draft Technical
Resolution on Entity Management.")
(put 'sgml-catalog-files 'sgml-type 'list);;
;;
;; SGML markup faces.
;;
(setq sgml-markup-faces
'((start-tag . font-lock-function-name-face)
(end-tag . font-lock-builtin-face)
(comment . font-lock-comment-face)
(pi . font-lock-keyword-face)
(sgml . font-lock-keyword-face)
(doctype . font-lock-keyword-face)
(entity . font-lock-variable-name-face)
(shortref . font-lock-variable-name-face)
(ignored  . font-lock-comment)
(ms-start . font-lock-type-face)
(ms-end . font-lock-type-face)))

(setq sgml-set-face t)

EOF


%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %{fname}.info

%_install_info %{fname}-api.info

%postun
%_remove_install_info %{fname}.info

%_remove_install_info %{fname}-api.info

%files
%defattr(-,root,root)
%doc README.psgml
%config(noreplace) %_sysconfdir/emacs/site-start.d/%{name}-init.el
%dir %{psgmldir}
%{psgmldir}/*
%dir %_libdir/sgml/cdtd
%_libdir/sgml/cdtd
%_infodir/*info*

