%define	fname	psgml
%define psgmldir %_datadir/emacs/site-lisp/psgml

%define debug_package %{nil}

Summary:	A GNU Emacs major mode for editing SGML documents
name:		emacs-%fname
Version:	1.3.2
Release: 	1
Requires: 	sgml-common
Requires: 	emacs >= 20.7
License: 	GPL
URL:		http://www.lysator.liu.se/projects/about_psgml.html
Source: 	ftp://ftp.lysator.liu.se:21/pub/sgml/ALPHA/psgml-%{version}.tar.gz
Group: 		Editors
Obsoletes:	psgml
Provides:	psgml = %version-%release
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
install -d %{buildroot}{%{psgmldir},%{_infodir},%{_libdir}/sgml/cdtd}

%makeinstall psgmldir=%{buildroot}%{psgmldir} lispdir=%{buildroot}%{psgmldir}

# Why putting source files ??????
#for i in $RPM_BUILD_ROOT%{psgmldir}/*.elc; do 
#  rm -f $i
#  cp `echo $(basename $i) | sed s/elc/el/` %{buildroot}%{psgmldir}
#done

make install-info infodir=%{buildroot}%{_infodir}

install -d %{buildroot}%{_sysconfdir}/emacs/site-start.d
cat << EOF > %{buildroot}%{_sysconfdir}/emacs/site-start.d/%{name}-init.el
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


%files
%doc README.psgml
%config(noreplace) %_sysconfdir/emacs/site-start.d/%{name}-init.el
%dir %{psgmldir}
%{psgmldir}/*
%_libdir/sgml/cdtd
%_infodir/*info*



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-11mdv2011.0
+ Revision: 618052
- the mass rebuild of 2010.0 packages

* Thu Sep 03 2009 Thierry Vignaud <tv@mandriva.org> 1.2.5-10mdv2010.0
+ Revision: 428587
- rebuild

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.2.5-9mdv2009.0
+ Revision: 266618
- rebuild early 2009.0 package (before pixel changes)

* Sun May 11 2008 Nicolas LÃ©cureuil <nlecureuil@mandriva.com> 1.2.5-8mdv2009.0
+ Revision: 205714
- Should not be noarch ed

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Thierry Vignaud <tv@mandriva.org> 1.2.5-7mdv2008.1
+ Revision: 132938
- fix prereq
- kill re-definition of %%buildroot on Pixel's request
- use %%mkrel
- fix summary-ended-with-dot
- import emacs-psgml


* Fri Apr 29 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.5-7mdk
- rebuild for new emacs

* Tue May 20 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.5-6mdk
- distlint fixes

* Tue Jan 21 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.5-5mdk
- rebuild for latest emacs

* Mon Jul 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.5-4mdk
- build release

* Fri Jun 21 2002 Götz Waschk <waschk@linux-mandrake.com> 1.2.5-3mdk
- buildrequires emacs-bin

* Sat Jun 01 2002 Yves Duret <yduret@mandrakesoft.com> 1.2.5-2mdk
- renamed to emacs-psgml to be more coherent with our other emacs modes.
- do not own %%_infodir in the rpm.
- %%setup -q
- spec clean up

* Thu May 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.5-1mdk
- new release
- add %%clean section

* Wed Jan 02 2002 Camille Begnis <camille@mandrakesoft.com> 1.2.4-1mdk
- 1.2.4
- removed patches

* Fri Nov 16 2001 Camille Begnis <camille@mandrakesoft.com> 1.2.2-4mdk
- Take patches from RedHat for DocBook>4.0 and emacs21
- Improve highlighting
- put again .elc files instead of .el 

* Fri Aug 31 2001 Lenny Cartier <lenny@mandrakesoft.com>  1.2.2-3mdk
- rebuild

* Fri Jun 22 2001 Pixel <pixel@mandrakesoft.com> 1.2.2-2mdk
- much cleanup (still doesn't work?)

* Wed Jun 21 2001 Camille Begnis <camille@mandrakesoft.com> 1.2.2-1mdk  
- Stole spec from RH

