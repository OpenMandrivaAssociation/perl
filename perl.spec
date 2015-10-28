%define threading 1
%define debugging 0

%if %{threading}
%define thread_arch -thread-multi
%endif

%define full_arch %{_arch}-%{_os}%{?thread_arch}
# Don't change to %{_libdir} as perl is clean and has arch-dependent subdirs
%define perl_root %{_prefix}/lib/perl5

%define	major 5.20

Summary:	The Perl programming language
Name:		perl
Epoch:		2
Version:	%{major}.3
Release:	1.1
License:	GPL+ or Artistic
Group:		Development/Perl
Url:		http://www.perl.org/
Source0:	http://www.cpan.org/src/%{name}-%{version}.tar.gz
Source1:	perl-headers-wanted
Source2:	perl-5.8.0-RC2-special-h2ph-not-failing-on-machine_ansi_header.patch
# macros
Source3:	perlbuild.macros
Source4:	libbuild.macros
#  make a package out of a perl pair of perl module, manpage and lib
Patch5:		perl-5.14.0-fix_eumm_append_to_config_cflags_instead_of_overriding.patch
Patch6:		perl-5.16.0-fix-LD_RUN_PATH-for-MakeMaker.patch
Patch14:	perl-5.20.1-install-files-using-chmod-644.patch
Patch15:	perl-5.16.0-lib64.patch
Patch16:	perl-5.16.0-perldoc-use-nroff-compatibility-option.patch
#(peroyvind) use -fPIC in stead of -fpic or else compile will fail on sparc (taken from redhat)
Patch21:	perl-5.8.1-RC4-fpic-fPIC.patch
Patch23:	perl-5.12.0-patchlevel.patch
Patch29:	perl-5.14.2-rpmdebug.patch
Patch32:	perl-5.10.0-incversionlist.patch
Patch38:	perl-donot-defer-sig11.patch

Patch43:	perl-5.12.0-RC0-skip-tests-using-dev-log-for-iurt.patch
Patch44:	perl-5.16.0-h2ph-handle-relative-include.patch

# mdvbz#34505, get rid of this patch as soon as possible :-/
Patch48:	perl-5.16.0-workaround-segfault-freeing-scalar-a-second-time.patch
Patch49:	perl-5.10.0-workaround-error-copying-freed-scalar.patch
Patch50:	perl-5.16.2-link-perl-extensions-against-libperl.patch
Patch51:	perl-5.20.2-add-soname-to-libperl.patch
#
# fixes taken from debian
#
# Fix a segmentation fault occurring in the mod_perl2 test suite (debian #475498, perl #33807)
Patch65:	local_symtab.diff
Patch66:	perl-5.20.0-USE_MM_LD_RUN_PATH.patch
# (tpg)https://rt.perl.org/Public/Bug/Display.html?id=121505
# gcc 4.9 by default does some optimizations that break perl
# add -fwrapv to ccflags
Patch68:	0001-perl-121505-add-fwrapv-to-ccflags-for-gcc-4.9-and-la.patch

# for NDBM
BuildRequires:	man
BuildRequires:	bzip2-devel
BuildRequires:	db5-devel
BuildRequires:	gdbm-devel
BuildRequires:	pkgconfig(zlib)

Requires:	perl-base = %{EVRD}
Conflicts:	perl-devel < 2:5.20.0

%define __noautoreq 'VMS'

%{expand:%%{load:%{SOURCE3}}}
%{expand:%%{load:%{SOURCE4}}}

%description
Perl is a high-level programming language with roots in C, sed, awk
and shell scripting.  Perl is good at handling processes and files,
and is especially good at handling text.  Perl's hallmarks are
practicality and efficiency.  While it is used to do a lot of
different things, Perl's most common applications (and what it excels
at) are probably system administration utilities and web programming.
A large proportion of the CGI scripts on the web are written in Perl.
You need the perl package installed on your system so that your
system can handle Perl scripts.

%package	base
Summary:	The Perl programming language (base)
Group:		Development/Perl
Provides:	perl(abi)
Provides:	perl(base)
# explicit file provides
Provides:	/usr/bin/perl
Conflicts:	perl < 2:5.20.3-1.1

%description	base
This is the base package for %{name}.


%{libpkg %{name} %{major}}

%package	devel
Summary:	The Perl programming language (devel)
Group:		Development/Perl
Requires:	%{name} = %{EVRD}
Requires:	perl(JSON::PP)

%description	devel
This is the devel package for %{name}.

%package	doc
Summary:	The Perl programming language (documentation)
Group:		Development/Perl
BuildArch:	noarch
Requires:	%{name} = %{EVRD}
Requires:	groff-base
Requires:	perl(Pod::Perldoc)

%description	doc
This is the documentation package for %{name}.
It contains also the 'perldoc' program.

%prep
%setup -q

%patch5 -p1 -b .flags~
%patch6 -p0
%patch14 -p1 -b .644~
%patch15 -p1 -b .lib64~
%patch16 -p0
%patch21 -p1 -b .peroyvind~
%patch23 -p0
%patch29 -p1 -b .rpmdebug~
%patch32 -p1
%patch38 -p0
%patch43 -p0
%patch44 -p1
%patch48 -p0 -b .doublefree~
%patch49 -p1
%patch50 -p1 -b .libperl~
%patch51 -p1 -b .soname~
%patch65 -p1
%patch66 -p1 -b .ldrunpath~

# fix linking against libperl during build
ln -s $PWD lib/CORE

# Configure Compress::Zlib to use system zlib
sed -i 's|BUILD_ZLIB      = True|BUILD_ZLIB      = False|
    s|INCLUDE         = ./zlib-src|INCLUDE         = %{_includedir}|
    s|LIB             = ./zlib-src|LIB             = %{_libdir}|' \
    cpan/Compress-Raw-Zlib/config.in

# Ensure that we never accidentally bundle zlib or bzip2
rm -rf cpan/Compress-Raw-Zlib/zlib-src
rm -rf cpan/Compress-Raw-Bzip2/bzip2-src
sed -i '/\(bzip2\|zlib\)-src/d' MANIFEST

%build
%ifarch aarch64
export AFLAGS="-Wl,--hash-style=both"
%endif
sh Configure -des \
  -Dinc_version_list="5.20.2 5.20.2/%{full_arch} 5.20.1 5.20.1/%{full_arch} 5.20.0 5.20.0/%{full_arch} 5.16.3 5.16.3/%{full_arch} 5.16.2 5.16.2/%{full_arch} 5.16.1 5.16.1/%{full_arch} 5.16.0 5.16.0/%{full_arch} 5.14.2 5.14.1 5.14.0 5.12.3 5.12.2 5.12.1 5.12.0" \
  -Darchname=%{_arch}-%{_os} \
  -Dcc='%{__cc}' \
%if %debugging
  -Doptimize="-O0" -DDEBUGGING="-g3 %{debugcflags}" \
%else
  -Doptimize="%{optflags}" -DDEBUGGING="%{debugcflags}" \
%endif
  -Dccdlflags="-fno-PIE %{ldflags} $AFLAGS -Wl,--warn-unresolved-symbols" \
  -Dcccdlflags="-fno-PIE -fPIC" \
  -Dldflags="%{ldflags} $AFLAGS" \
  -Dlddlflags="-shared -fno-PIE %{optflags} %{ldflags} $AFLAGS -Wl,--warn-unresolved-symbols" \
  -Dcppflags="-D_REENTRANT -D_GNU_SOURCE" \
  -Dlibpth='%{_libdir} /%{_lib}' \
  -Dprefix=%{_prefix} -Dvendorprefix=%{_prefix} \
  -Dsiteprefix=%{_prefix} -Dsitebin=%{_prefix}/local/bin \
  -Dsiteman1dir=%{_prefix}/local/share/man/man1 \
  -Dsiteman3dir=%{_prefix}/local/share/man/man3 \
  -Dman3dir=%{_mandir}/man3pm \
  -Dvendorman3dir=%{_mandir}/man3 \
  -Dman3ext=3pm \
  -Dcf_by="%{vendor}" -Dmyhostname=localhost -Dperladmin=root@localhost -Dcf_email=root@localhost \
  -Dperllibs='-lnsl -ldl -lm -lcrypt -lutil -lc -lpthread'   \
  -Ud_csh \
  -Duseshrplib \
  -Duselargefiles \
  -Dpager='%{_bindir}/less -isr' \
%if %threading
  -Duseithreads \
  -Dusethreads \
%endif
%ifarch %{sparc}
  -Ud_longdbl \
%endif
  -Di_db \
  -Di_ndbm \
  -Di_gdbm
#  -Dnoextensions='Archive/Extract Archive/Tar CGI Compress/Raw/Bzip2 Compress/Raw/Zlib CPANPLUS/Dist/Build CPANPLUS Digest/SHA IO/Compress JSON/PP Pod/Perldoc Module/Build Module/CoreList Pod/Perldoc Term/UI Time/Piece'

# workaround for not using colorgcc that relies on perl
PATH="${PATH#%{_datadir}/colorgcc:}"

# (tpg) do not build bzip
BUILD_BZIP2=0
BZIP2_LIB=%{_libdir}
export BUILD_BZIP2 BZIP2_LIB

%make

%check
# This test relies on Digest::SHA being available
rm -f t/porting/regen.t
sed -i -e '/^t\/porting\/regen.t/d' MANIFEST

# FIXME: should pick up library path automatically in patch..
export LIBRARY_PATH="$PWD"
RPM_BUILD_ROOT="" TEST_JOBS=%(/usr/bin/getconf _NPROCESSORS_ONLN) make test_harness_notty CCDLFLAGS=

%install
%makeinstall_std

install -d %{buildroot}%{perl_root}/

# We prefer 0755 instead of 0555
find %{buildroot} -name "*.so" | xargs chmod 0755

cp -f utils/h2ph utils/h2ph_patched
cat %{SOURCE2} | patch -p1

# LD_PRELOAD doesn't work... why?
LD_LIBRARY_PATH=`pwd` ./perl -Ilib utils/h2ph_patched -a -d %{buildroot}%{perl_root}/%{version}/%{full_arch} `cat %{SOURCE1}` > /dev/null ||:

# i don't like hardlinks, having symlinks instead:
ln -sf perl5 %{buildroot}%{_bindir}/perl
ln -s perl%{version} %{buildroot}%{_bindir}/perl5

rm %{buildroot}%{_bindir}/perlivp %{buildroot}%{_mandir}/man1/perlivp.1

%ifarch ppc
perl -ni -e 'print if !/sub __syscall_nr/' %{buildroot}%{perl_root}/%{version}/%{full_arch}/asm/unistd.ph
perl -ni -e 'print unless m/sub __syscall_nr/' %{buildroot}/%{perl_root}/%{version}/%{full_arch}/asm/unistd.ph
%endif

# work in progress..
chmod u+w -R %{buildroot}
# Get rid of stuff from Archive::Tar - the standalone package is released
# far more frequently
rm -r	%{buildroot}%{_bindir}/ptar \
	%{buildroot}%{_bindir}/ptardiff \
	%{buildroot}%{_bindir}/ptargrep \
	%{buildroot}%{perl_root}/%{version}/Archive/Tar.pm \
	%{buildroot}%{perl_root}/%{version}/Archive/Tar \
	%{buildroot}%{_mandir}/man1/ptar.1 \
	%{buildroot}%{_mandir}/man1/ptardiff.1 \
	%{buildroot}%{_mandir}/man1/ptargrep.1 \
	%{buildroot}%{_mandir}/man3pm/Archive::Tar* 

# idem Digest::SHA
rm -r	%{buildroot}%{_bindir}/shasum \
	%{buildroot}%{perl_root}/%{version}/%{full_arch}/Digest/SHA.pm \
	%{buildroot}%{perl_root}/%{version}/%{full_arch}/auto/Digest/SHA \
	%{buildroot}%{_mandir}/man1/shasum.1 \
	%{buildroot}%{_mandir}/man3pm/Digest::SHA.3* \

# Pod::Perldoc
rm -r	%{buildroot}%{_bindir}/perldoc \
	%{buildroot}%{perl_root}/%{version}/pod/perldoc.pod \
	%{buildroot}%{perl_root}/%{version}/Pod/Perldoc.pm \
	%{buildroot}%{perl_root}/%{version}/Pod/Perldoc/ \
	%{buildroot}%{_mandir}/man1/perldoc.1* \
	%{buildroot}%{_mandir}/man3pm/Pod::Perldoc*

# Time::Piece
rm -r	%{buildroot}%{perl_root}/%{version}/%{full_arch}/Time/Piece.pm \
	%{buildroot}%{perl_root}/%{version}/%{full_arch}/Time/Seconds.pm \
	%{buildroot}%{perl_root}/%{version}/%{full_arch}/auto/Time/Piece/ \
	%{buildroot}%{_mandir}/man3pm/Time::Piece.3* \
	%{buildroot}%{_mandir}/man3pm/Time::Seconds.3*

# CGI
rm -r	%{buildroot}%{perl_root}/%{version}/CGI \
	%{buildroot}%{perl_root}/%{version}/CGI.pm \
	%{buildroot}%{_mandir}/man3pm/CGI.3* \
	%{buildroot}%{_mandir}/man3pm/CGI::*.3*

# Compress::Raw::Bzip2
rm -r	%{buildroot}%{perl_root}/%{version}/%{full_arch}/Compress/Raw/Bzip2.pm \
	%{buildroot}%{perl_root}/%{version}/%{full_arch}/auto/Compress/Raw/Bzip2 \
	%{buildroot}%{_mandir}/man3pm/Compress::Raw::Bzip2*

# Compress::Raw::Zlib
rm -r	%{buildroot}%{perl_root}/%{version}/%{full_arch}/Compress/Raw/Zlib.pm \
	%{buildroot}%{perl_root}/%{version}/%{full_arch}/auto/Compress/Raw/Zlib \
	%{buildroot}%{_mandir}/man3pm/Compress::Raw::Zlib*

# IO::Compress
rm -r	%{buildroot}%{_bindir}/zipdetails \
	%{buildroot}%{_mandir}/man1/zipdetails.* \
	%{buildroot}%{perl_root}/%{version}/Compress/Zlib.pm \
	%{buildroot}%{_mandir}/man3pm/Compress::Zlib* \
	%{buildroot}%{perl_root}/%{version}/File/GlobMapper.pm \
	%{buildroot}%{_mandir}/man3pm/File::GlobMapper.* \
	%{buildroot}%{perl_root}/%{version}/IO/Compress \
	%{buildroot}%{perl_root}/%{version}/IO/Uncompress \
	%{buildroot}%{_mandir}/man3pm/IO::Compress* \
	%{buildroot}%{_mandir}/man3pm/IO::Uncompress*

# JSON::PP
rm  -r	%{buildroot}%{_bindir}/json_pp \
	%{buildroot}%{perl_root}/%{version}/JSON/PP \
	%{buildroot}%{perl_root}/%{version}/JSON/PP.pm \
	%{buildroot}%{_mandir}/man1/json_pp.1* \
	%{buildroot}%{_mandir}/man3pm/JSON::PP.3* \
	%{buildroot}%{_mandir}/man3pm/JSON::PP::Boolean.3pm*

# Module::Build
rm  -r	%{buildroot}%{_bindir}/config_data \
	%{buildroot}%{perl_root}/%{version}/inc/ \
	%{buildroot}%{perl_root}/%{version}/Module/Build/ \
	%{buildroot}%{perl_root}/%{version}/Module/Build.pm \
	%{buildroot}%{_mandir}/man1/config_data.1* \
	%{buildroot}%{_mandir}/man3pm/Module::Build* \
	%{buildroot}%{_mandir}/man3pm/inc::latest.3*

# perl-Module-CoreList - seems like
rm -rf %{buildroot}%{_bindir}/corelist \
	%{buildroot}%{perl_root}/%{version}/CoreList \
	%{buildroot}%{perl_root}/%{version}/CoreList.pm \
	%{buildroot}%{perl_root}/%{version}/CoreList.pod \
	%{buildroot}%{perl_root}/%{version}/CoreList.pm \
	%{buildroot}%{_mandir}/man1/corelist.1*

# call spec-helper before creating the file list
# (spec-helper removes some files, and compress some others)
%define dont_strip 1
%{?__spec_helper_post}
%undefine dont_strip

rm -fr perl.list perl-doc.list perl-base.list perl-devel.list

find %{buildroot}%{perl_root}/%{version} "(" -name "*.pod" -o -iname "Changes*" -o -iname "ChangeLog*" -o -iname "README*" ")" -a -not -name "*.e2x" -printf "%%%%doc %%p\n" |sort -u >> perl-doc.list
find %{buildroot}%{_mandir}/man1 ! -name \perlivp.1* ! -type d >> perl.list
find %{buildroot}%{perl_root}/%{version} -name \*.ph -a ! \( -name \unistd*.ph -o -name \syscall.ph -o -name \wordsize.ph -o -name \_h2ph_pre.ph \) >> perl.list
find %{buildroot}%{perl_root}/%{version} -name \*.e2x >> perl-devel.list
sed -e 's#%{buildroot}##g' -i perl*.list

#MD file listed twice
for i in $(ls perl*.list); do cat $i | sort -u > tmp.list; mv -f tmp.list $i; done
rm -f %{buildroot}%{perl_root}/%{version}/%{full_arch}/CORE/libperl.so*

%files base
%dir %{perl_root}
%{perldir -dl}
%{perldir -dn}
%{perldir -d}
%{perldir -dl arybase}
%{perldir -dl attributes}
%{perldir -dl mro}
%{perldir -dl re}
%{perldir -dl sdbm}
%{perldir -dl threads}
%{perldir -dl threads-shared}
%{perldir -d CORE}
%{perldir -d asm}
%{perldir -d bits}
%{perldir -d sys}
%{perldir -d threads}
%{perldir -dn autodie}
%{perldir -dn encoding}
%{perldir -dn overload}
%{perldir -dn unicore}
%{perldir -dn version}
%{perldir -dn warnings}
%{_bindir}/perl
%{_bindir}/perl%{version}
%{_bindir}/perl5
%{perldir}/_h2ph_pre.ph
%{perldir}/asm/unistd*.ph
%{perldir}/bits/syscall.ph
%{perldir}/bits/wordsize.ph
%{perldir}/sys/syscall.ph
%{perldir}/syscall.ph
%{perldir -n}/unicore/To/Fold.pl
%{perldir -n}/unicore/To/Lower.pl
%{perldir -n}/unicore/To/Upper.pl
#noprovides
%{perlpairs -n autodie}
%{perlpairs -n autodie-exception}
%{perlpairs -n autodie-exception-system}
%{perlpairs -n autodie-hints}
%{perlpairs -n autodie-skip}
%{perlpairs -n autouse}
%{perlpairs -n base}
%{perlpairs -n bigint}
%{perlpairs -n bignum}
%{perlpairs -n bigrat}
%{perlpairs -n blib}
%{perlpairs -n bytes}
%{perldir -n}/bytes_heavy.pl
%{perlpairs -n charnames}
%{perldir -n _charnames}
%{perlpairs -n constant}
%{perlpairs -n deprecate}
%{perlpairs -n diagnostics}
%{perlpairs -n encoding-warnings}
%{perlpairs -n experimental}
%{perlpairs -n feature}
%{perlpairs -n fields}
%{perlpairs -n filetest}
%{perlpairs -n if}
%{perlpairs -n integer}
%{perlpairs -n less}
%{perlpairs -n locale}
%{perlpairs -n open}
%{perlpairs -n overload}
%{perldir -n overload-numbers}
%{perlpairs -n overloading}
%{perlpairs -n parent}
%{perlpairs -n sigtrap}
%{perlpairs -n sort}
%{perlpairs -n strict}
%{perlpairs -n subs}
%{perlpairs -n utf8}
%{perldir -n}/utf8_heavy.pl
%{perlpairs -n vars}
%{perlpairs -n version}
%{perldir -n version-regex}
%{perldir -n version-vpp}
%{mandir3pm version-Internals}
%{perlpairs -n vmsish}
%{perlpairs -n warnings}
%{perlpairs -n warnings-register}
%{perlpairs  encoding}
%{perlpairs  lib}
%{perlpairs  ops}
%{perlpairs -l arybase}
%{perlpairs -l attributes}
%{perlpairs -l mro}
%{perlpairs -l re}
%{perlpairs -l threads}
%{perlpairs -l threads-shared}

%files -f perl.list
%doc README
%{_bindir}/a2p
%{_bindir}/find2perl
%{_bindir}/perlbug
%{_bindir}/perlthanks
%{_bindir}/pod2html
%{_bindir}/pod2man
%{_bindir}/pod2text
%{_bindir}/prove
%{_bindir}/s2p
%{_bindir}/splain
%{perldir -l}/sdbm/extralibs.ld
%{perldir -n Pod-Functions}
%{perldir -n}/dumpvar.pl
%{perldir -n}/perl5db.pl
%{perldir -n perlfaq}
%{perldir -n}/unicore/*
%exclude %{perldir -n}/unicore/To/Fold.pl
%exclude %{perldir -n}/unicore/To/Lower.pl
%exclude %{perldir -n}/unicore/To/Upper.pl

%files devel -f perl-devel.list
%{_bindir}/c2ph
%{_bindir}/cpan
%{_bindir}/enc2xs
%{_bindir}/h2ph
%{_bindir}/h2xs
%{_bindir}/instmodsh
%{_bindir}/libnetcfg
%{_bindir}/piconv
%{_bindir}/pl2pm
%{_bindir}/pod2usage
%{_bindir}/podchecker
%{_bindir}/podselect
%{_bindir}/psed
%{_bindir}/pstruct
%{_bindir}/xsubpp
%{perl_root}/%{version}/Encode/encode.h
%{perl_root}/%{version}/ExtUtils/xsubpp
%{perl_root}/%{version}/%{full_arch}/CORE/*.h
%{_libdir}/libperl.so

%files doc -f perl-doc.list
%{mandir3pm CORE}
%{mandir3pm ExtUtils-XSSymSet}
%{mandir3pm Encode-PerlIO}
%{mandir3pm Encode-Supported}

#MD split perl pkgs
%{perlpkg -n AnyDBM_File}
%{perlpkg -n App-Cpan}
%{perlpkg -n App-Prove}

%{perlpkg -n App-Prove-State}
%{perlpairs -n App-Prove-State-Result}
%{perlpairs -n App-Prove-State-Result-Test}

%{perlpkg -n Attribute-Handlers}
%{perlpkg -n AutoLoader}
%{perlpkg -n AutoSplit}
%{perlpkg -n Benchmark}

%{perlpkg -ng CPAN}
%{perldir -n CPAN-Exception-RecursiveDependency}
%{perldir -n CPAN-Exception-blocked_urllist}
%{perldir -n CPAN-Exception-yaml_not_installed}
%{perldir -n CPAN-Exception-yaml_process_error}
%{perldir -n CPAN-FTP-netrc}
%{perldir -n CPAN-HTTP-Client}
%{perldir -n CPAN-HTTP-Credentials}
%{perldir -n}/CPAN/Kwalify/distroprefs.dd
%{perldir -n}/CPAN/Kwalify/distroprefs.yml
%{perldir -n CPAN-LWP-UserAgent}
%exclude %{perldir -n}/CPAN/Meta*
%exclude %{mandir3pm CPAN-Meta*}

%{perlpkg -ng CPAN-Meta}
%{perlpkg -ng Carp}
%{perlpkg -n Class-Struct}
%{perlpkg -n Config-Extensions}
%{perlpkg -n Config-Perl-V}
%{perlpkg -n DB}
%{perlpkg -ng DBM_Filter}
%{perlpkg -n Devel-SelfStubber}

%{perlpkg -n Digest}
%{perlpairs -n Digest-base}
%{perlpairs -n Digest-file}

%{perlpkg -n DirHandle}
%{perlpkg -n Dumpvalue}
%{perlpkg -n English}
%{perlpkg -n Env}
%{perlpkg -ng Exporter}

%{perlpkg -n ExtUtils-CBuilder}
%{perldir -dn ExtUtils-CBuilder}
%{perldir -n ExtUtils-CBuilder-Base}

%{perlglob -n ExtUtils-CBuilder-Platform}
%{perldir -dn ExtUtils-CBuilder-Platform-Windows}
%{perldir -n ExtUtils-CBuilder-Platform-Windows-*}

%{perlpkg -n ExtUtils-Command}
%{perlpkg -n ExtUtils-Command-MM}

%{perlpkg -n ExtUtils-Constant}
%{perldir -dn ExtUtils-Constant}
%{perldir -n ExtUtils-Constant-ProxySubs}

%{perlpkg -n ExtUtils-Constant-Base}
%{perlpkg -n ExtUtils-Constant-Utils}
%{perlpkg -n ExtUtils-Constant-XS}
%{perlpkg -n ExtUtils-Embed}
%{perlpkg -n ExtUtils-Install}
%{perlpkg -n ExtUtils-Installed}
%{perlpkg -ng ExtUtils-Liblist}
%{perlpkg -ng ExtUtils-MakeMaker}
%{perlpkg -n ExtUtils-MM}
%{perlpkg -n ExtUtils-MM_AIX}
%{perlpkg -n ExtUtils-MM_Any}
%{perlpkg -n ExtUtils-MM_BeOS}
%{perlpkg -n ExtUtils-MM_Cygwin}
%{perlpkg -n ExtUtils-MM_DOS}
%{perlpkg -n ExtUtils-MM_Darwin}
%{perlpkg -n ExtUtils-MM_MacOS}
%{perlpkg -n ExtUtils-MM_NW5}
%{perlpkg -n ExtUtils-MM_OS2}
%{perlpkg -n ExtUtils-MM_QNX}
%{perlpkg -n ExtUtils-MM_UWIN}
%{perlpkg -n ExtUtils-MM_Unix}
%{perlpkg -n ExtUtils-MM_VMS}
%{perlpkg -n ExtUtils-MM_VOS}
%{perlpkg -n ExtUtils-MM_Win32}
%{perlpkg -n ExtUtils-MM_Win95}
%{perlpkg -n ExtUtils-MY}
%{perlpkg -n Fatal}

%{perlpkg -n ExtUtils-Manifest}
%{perldir -n}/ExtUtils/MANIFEST.SKIP

%{perlpkg -n ExtUtils-Miniperl}
%{perlpkg -n ExtUtils-Mkbootstrap}
%{perlpkg -n ExtUtils-Mksymlists}
%{perlpkg -n ExtUtils-Packlist}
%{perlpkg -ng ExtUtils-ParseXS}

%{perlpkg -ng ExtUtils-Typemaps}
%{perldir -n}/ExtUtils/typemap

%{perlpkg -n ExtUtils-testlib}
%{perlpkg -n File-Compare}
%{perlpkg -n File-Copy}
%{perlpkg -n File-Fetch}
%{perlpkg -n File-stat}
%{perlpkg -n File-Basename}
%{perlpkg -n File-Find}
%{perlpkg -n File-Path}
%{perlpkg -n File-Temp}
%{perlpkg -n FileCache}
%{perlpkg -n Filter-Simple}
%{perlpkg -n FileHandle}
%{perlpkg -n FindBin}
%{perlpkg -n Getopt-Long}
%{perlpkg -n Getopt-Std}
%{perlpkg -n HTTP-Tiny}
%{perlpkg -n I18N-LangTags}
%{perlpkg -n I18N-LangTags-Detect}
%{perlpkg -n I18N-LangTags-List}
%{perlpkg -n I18N-Collate}
%{perlpkg -n IO-Zlib}
%{perlpkg -n IPC-Cmd}
%{perlpkg -n IPC-Open2}
%{perlpkg -n IPC-Open3}
%{perlpkg -ng Locale-Codes}
%{perlpkg -n Locale-Country}
%{perlpkg -n Locale-Currency}
%{perlpkg -n Locale-Language}
%{perlpkg -n Locale-Script}
%{perlpkg -ng Locale-Maketext}
%{perlpkg -ng Math-BigFloat}

%{perlpkg -n Math-BigInt}
%{perldir -dn Math-BigInt}
%{perldir -n Math-BigInt-Trace}

%{perlpkg -n Math-BigInt-Calc}
%{perlpkg -n Math-BigInt-CalcEmu}
%{perlpkg -n Math-BigRat}
%{perlpkg -n Math-Complex}
%{perlpkg -n Math-Trig}
%{perlpkg -ng Memoize}

%{perlpkg -n Module-CoreList}
%{perldir -dn Module-CoreList}
%{perldir -n Module-CoreList-TieHashDelta}

%{perlpkg -n Module-CoreList-Utils}
%{perlpkg -ng Module-Load}
%{perlpkg -n Module-Loaded}
%{perlpkg -n Module-Metadata}
%{perlpkg -n Net-Cmd}

%{perlpkg -n Net-Config}
%{mandir3pm Net-libnetFAQ}
%{perlpairs -n Net-hostent}
%{perlpairs -n Net-netent}
%{perlpairs -n Net-protoent}
%{perlpairs -n Net-servent}

%{perlpkg -n Net-Domain}
%{perlpkg -ng Net-FTP}
%{perlpkg -n Net-NNTP}
%{perlpkg -n Net-Netrc}
%{perlpkg -n Net-POP3}
%{perlpkg -n Net-Ping}
%{perlpkg -n Net-SMTP}
%{perlpkg -n Net-Time}
%{perlpkg -n NEXT}
%{perlpkg -n Package-Constants}
%{perlpkg -n Params-Check}
%{perlpkg -n Parse-CPAN-Meta}
%{perlpkg -n Perl-OSType}

%{perlpkg -n PerlIO}
%{perlpairs -n PerlIO-via-QuotedPrint}

%{perlpkg -n Pod-Checker}
%{perlpkg -n Pod-Escapes}
%{perlpkg -n Pod-Find}
%{perlpkg -n Pod-Html}
%{perlpkg -n Pod-InputObjects}
%{perlpkg -n Pod-Man}
%{perlpkg -n Pod-ParseLink}
%{perlpkg -n Pod-ParseUtils}
%{perlpkg -n Pod-Parser}
%{perlpkg -n Pod-PlainText}
%{perlpkg -n Pod-Select}
%{perlpkg -n Pod-Usage}

%{perlpkg -ng Pod-Simple}
%{perlpkg -ng Pod-Text}
%{perlpkg -n Safe}
%{perlpkg -n Search-Dict}
%{perlpkg -n SelectSaver}
%{perlpkg -n SelfLoader}
%{perlpkg -n Symbol}

%{perlpkg -n TAP-Parser}
%{perlpairs -n TAP-Parser-Aggregator}
%{perlpairs -ns TAP-Parser-Grammar}
%{perlpairs -ns TAP-Parser-Iterator}
%{perlpairs -ns TAP-Parser-IteratorFactory}
%{perlpairs -n TAP-Parser-Iterator-Array}
%{perlpairs -ns TAP-Parser-Iterator-Process}
%{perlpairs -ns TAP-Parser-Iterator-Stream}
%{perlpairs -ns TAP-Parser-Multiplexer}
%{perlpairs -ns TAP-Parser-Result}
%{perlpairs -ns TAP-Parser-ResultFactory}
%{perlpairs -n TAP-Parser-Result-Bailout}
%{perlpairs -ns TAP-Parser-Result-Comment}
%{perlpairs -ns TAP-Parser-Result-Plan}
%{perlpairs -ns TAP-Parser-Result-Pragma}
%{perlpairs -ns TAP-Parser-Result-Test}
%{perlpairs -ns TAP-Parser-Result-Unknown}
%{perlpairs -ns TAP-Parser-Result-Version}
%{perlpairs -ns TAP-Parser-Result-YAML}
%{perlpairs -ns TAP-Parser-Scheduler}
%{perlpairs -n TAP-Parser-Scheduler-Job}
%{perlpairs -ns TAP-Parser-Scheduler-Spinner}
%{perlpairs -ns TAP-Parser-Source}
%{perlpairs -ns TAP-Parser-SourceHandler}
%{perlpairs -n TAP-Parser-SourceHandler-Executable}
%{perlpairs -ns TAP-Parser-SourceHandler-File}
%{perlpairs -ns TAP-Parser-SourceHandler-Handle}
%{perlpairs -ns TAP-Parser-SourceHandler-Perl}
%{perlpairs -ns TAP-Parser-SourceHandler-RawTAP}
%{perlpairs -n TAP-Parser-YAMLish-Reader}
%{perlpairs -ns TAP-Parser-YAMLish-Writer}

%{perlpkg -n TAP-Base}

%{perlglob -n TAP-Formatter}
%{perldir -dn TAP-Formatter-Console}
%{perldir -dn TAP-Formatter-File}
%{perldir -n TAP-Formatter-Console-ParallelSession}
%{perldir -n TAP-Formatter-Console-Session}
%{perldir -n TAP-Formatter-File-Session}

%{perlpkg -n TAP-Harness}
%{perlpairs -n TAP-Harness-Env}
%{mandir3pm TAP-Harness-Beyond}

%{perlpkg -n TAP-Object}

%{perlpkg -n Test}
%{perlpairs -n Test-Builder}
%{perlpairs -n Test-Builder-Module}
%{perlpairs -ns Test-Builder-Tester}
%{perlpairs -n Test-Builder-Tester-Color}
%{perlpairs -n Test-Harness}
%{perlpairs -n Test-More}
%{perlpairs -n Test-Simple}
%{mandir3pm Test-Tutorial}

%{perlpkg -n Term-ANSIColor}
%{perlpkg -n Term-Cap}
%{perlpkg -n Term-Complete}
%{perlpkg -n Term-ReadLine}
%{perlpkg -n Text-Abbrev}
%{perlpkg -n Text-Balanced}
%{perlpkg -n Text-ParseWords}
%{perlpkg -n Text-Tabs}
%{perlpkg -n Text-Wrap}
%{perlpkg -ng Thread}
%{perlpkg -n Tie-Array}
%{perlpkg -n Tie-File}
%{perlpkg -n Tie-Handle}
%{perlpkg -n Tie-Hash}
%{perlpkg -n Tie-Memoize}
%{perlpkg -n Tie-RefHash}
%{perlpkg -n Tie-Scalar}
%{perlpkg -n Tie-StdHandle}
%{perlpkg -n Tie-SubstrHash}

%{perlglob -n Time}
%exclude %{mandir3pm Time-HiRes}

%{perlpkg -n UNIVERSAL}
%{perlpkg -n Unicode-UCD}
%{perlglob -n User}
%{perlpkg -n XSLoader}

#arched
%{perlpkg -l B}
%{perlpairs -n B-Debug}
%{perlpairs -n B-Deparse}
%{perlpairs B-Concise}
%{perlpairs B-Showlex}
%{perlpairs B-Terse}
%{perlpairs B-Xref}

%{perlpkg -l Cwd}
%{perlpkg -l DB_File}
%{perlpkg -l Data-Dumper}
%{perlpkg -l Devel-PPPort}
%{perlpkg -l Devel-Peek}
%{perlpkg -l Digest-MD5}

%{perlpkg -l Encode}
%{perlpairs Encode-Alias}
%{perlpairs Encode-CJKConstants}
%{perlpairs Encode-Config}
%{perlpairs Encode-Encoder}
%{perlpairs Encode-Encoding}
%{perlpairs Encode-GSM0338}
%{perlpairs Encode-Guess}

%{perlpkg -l Encode-Byte}
%{perlpkg -lg Encode-CN}
%{perlpkg -l Encode-EBCDIC}
%{perlpkg -lg Encode-JP}
%{perlpkg -lg Encode-KR}
%{perlpkg -l Encode-Symbol}
%{perlpkg -l Encode-TW}
%{perlpkg -lg Encode-Unicode}
%{perlpkg -l Fcntl}
%{perlpkg -l File-DosGlob}
%{perlpkg -l File-Glob}
%{perlpkg -l Filter-Util-Call}
%{perlpkg -l GDBM_File}
%{perlpkg -l Hash-Util}
%{perlpkg -l Hash-Util-FieldHash}
%{perlpkg -l I18N-Langinfo}
%{perlpkg -l IO}
%{perlpkg IO-File}
%{perlpkg IO-Handle}
%{perlpkg IO-Seekable}
%{perlpkg IO-Select}
%{perlpkg IO-Socket}
%{perlpkg IO-Socket-INET}
%{perlpkg IO-Socket-UNIX}
%{perlpkg IO-Dir}
%{perlpkg IO-Pipe}
%{perlpkg IO-Poll}
%{perlpkg -n IO-Socket-IP}
%{perlpkg -l IPC-SysV}
%{perlpkg -lg List-Util}
%{perlpkg -l MIME-Base64}
%{perlpkg -l Math-BigInt-FastCalc}
%{perlpkg -l NDBM_File}
%{perlpkg -l ODBM_File}
%{perlpkg -l Opcode}
%{perlpkg -l POSIX}
%{perlpkg -l PerlIO-encoding}
%{perlpkg -l PerlIO-mmap}
%{perlpkg -l PerlIO-scalar}
%{perlpkg -l PerlIO-via}
%{perlpkg -l SDBM_File}
%{perlpkg -l Socket}
%{perlpkg -l Storable}
%{perlpkg -l Sys-Hostname}
%{perlpkg -l Sys-Syslog}
%{perlpkg -l Tie-Hash-NamedCapture}
%{perlpkg -l Time-HiRes}

%{perlpkg -l Unicode-Collate}
%{perlpairs Unicode-Collate-Locale}
%{perldir -n}/Unicode/Collate/Locale/*pl
%{perlpairs -n Unicode-Collate-CJK-Big5}
%{perlpairs -ns Unicode-Collate-CJK-GB2312}
%{perlpairs -ns Unicode-Collate-CJK-JISX0208}
%{perlpairs -ns Unicode-Collate-CJK-Korean}
%{perlpairs -ns Unicode-Collate-CJK-Pinyin}
%{perlpairs -ns Unicode-Collate-CJK-Stroke}
%{perlpairs -ns Unicode-Collate-CJK-Zhuyin}
%{perldir -n}/Unicode/Collate/*.txt

%{perlpkg -l Unicode-Normalize}

#no libs in arched pkg
%{perlpkg Config}
%{perldir}/Config_git.pl
%{perldir}/Config_heavy.pl

%{perlpkg DynaLoader}

%{perlglob Encode-MIME}
%{perldir -d Encode-MIME-Header}
%{perldir Encode-MIME-Header-ISO_2022_JP}

%{perlpkg Errno}
%{perlpkg -g File-Spec}
%{perlpkg MIME-QuotedPrint}
%{perlpkg IPC-Msg}
%{perlpkg IPC-Semaphore}
%{perlpkg IPC-SharedMem}
%{perlpkg O}
%{perlpkg Scalar-Util}

