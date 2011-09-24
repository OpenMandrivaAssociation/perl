%define threading 1
%define debugging 0

#%%define _default_patch_fuzz 2

%if %threading
%define thread_arch -thread-multi
%else
%define thread_arch %{nil}
%endif

%define arch %(echo %{_arch} | sed -e "s/amd64/x86_64/")
%define full_arch %{arch}-%{_os}%{thread_arch}
# Don't change to %{_libdir} as perl is clean and has arch-dependent subdirs
%define perl_root %{_prefix}/lib/perl5

Name:     perl
Version:  5.12.3
#Release:  %mkrel 0.RC4.2
Release:  %mkrel 9
Epoch:    2

%define rel %{nil}
#define rel -RC4

Summary:  The Perl programming language
License:  GPL+ or Artistic
Group:    Development/Perl
Url:      http://www.perl.org/

# ftp://ftp.funet.fi/pub/languages/perl/snap/perl@17574.tbz
#ftp://ftp.funet.fi/pub/languages/perl/CPAN/src/perl-%{version}.tar.bz2
Source0:  http://www.cpan.org/src/perl-%{version}%{rel}.tar.gz
Source1:  perl-headers-wanted
Source2:  perl-5.8.0-RC2-special-h2ph-not-failing-on-machine_ansi_header.patch
Patch6:   perl-5.12.0-RC0-fix-LD_RUN_PATH-for-MakeMaker.patch
Patch14:  perl-5.12.0-RC0-install-files-using-chmod-644.patch
Patch15:  perl-5.10.1-RC1-lib64.patch
Patch16:  perl-5.12.0-RC0-perldoc-use-nroff-compatibility-option.patch
#(peroyvind) use -fPIC in stead of -fpic or else compile will fail on sparc (taken from redhat)
Patch21:  perl-5.8.1-RC4-fpic-fPIC.patch
Patch23:  perl-5.12.0-patchlevel.patch
Patch29:  perl-5.12.0-RC0-rpmdebug.patch
Patch32:  perl-5.10.0-incversionlist.patch
Patch38:  perl-donot-defer-sig11.patch

Patch43:  perl-5.12.0-RC0-skip-tests-using-dev-log-for-iurt.patch
Patch44:  perl-5.10.1-RC1-h2ph--handle-relative-include.patch

# mdvbz#34505, get rid of this patch as soon as possible :-/
Patch48:  perl-5.10.0-workaround-segfault-freeing-scalar-a-second-time.patch
Patch49:  perl-5.10.0-workaround-error-copying-freed-scalar.patch
# mdv#60956 - fix h2ph
Patch50:  perl-5.12.2-fix-h2ph.patch
# (oe) http://rt.perl.org/rt3/Public/Bug/Display.html?id=74088
Patch51: 0001-perl-74088.patch
# (oe) http://rt.perl.org/rt3/Public/Bug/Display.html?id=87336
Patch52: perl-5.12.3-CVE-2011-1487.diff

#
# fixes taken from debian
#
# Fix a segmentation fault occurring in the mod_perl2 test suite (debian #475498, perl #33807)
Patch65:  local_symtab.diff

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}

Requires: perl-base = %{epoch}:%{version}-%{release}

# the following modules are part of perl normally, but are shipped in
# separated rpm packages. let's require them in order to please people
# that think that installing "perl" will have a full perl as shipped by
# upstream. (cf tom christiansen and the lengthy thread:
# http://www.nntp.perl.org/group/perl.perl5.porters/2009/08/msg149747.html)
Suggests: perl-Archive-Extract
Suggests: perl-Archive-Tar
Suggests: perl-CGI
Suggests: perl-CPANPLUS
Suggests: perl-CPANPLUS-Dist-Build
Suggests: perl-Digest-SHA
Suggests: perl-Module-Build
Suggests: perl-Module-CoreList
Suggests: perl-Time-Piece

Provides: perl(getopts.pl)
Provides: perl(ctime.pl)
Provides: perl(flush.pl)
Provides: perl(find.pl)

Provides: perl(attributes)
Provides: perl(fields)
Provides: perl(if)
Provides: perl(locale)
Provides: perl(subs)

Provides:  perl-MIME-Base64 = 3.080.0
Obsoletes: perl-MIME-Base64 < 3.080.0
Provides:  perl-libnet
Provides:  perl-Storable = 2.200.0
Obsoletes: perl-Storable < 2.200.0
Provides:  perl-Digest-MD5 = 2.390.0
Obsoletes: perl-Digest-MD5 < 2.390.0
Provides:  perl-Time-HiRes = 1:1.971.900
Obsoletes: perl-Time-HiRes < 1:1.971.900
Provides:  perl-Locale-Codes
Provides:  perl-Test-Simple = 0.920.0
Obsoletes: perl-Test-Simple < 0.920.0
Provides:  perl-Test-Builder-Tester = 1.180.0
Obsoletes: perl-Test-Builder-Tester < 1.180.0

Provides:  perl(version) = 1:0.74
Provides:  perl-version = 1:0.74
Obsoletes: perl-version < 1:0.74
Provides:  perl-File-Fetch = 0.14
Obsoletes: perl-File-Fetch < 0.14
Provides:  perl-CPAN = 1.9205
Obsoletes: perl-CPAN < 1.9205
Provides:  perl-IO-Zlib = 1.07
Obsoletes: perl-IO-Zlib < 1.07
Provides:  perl-Pod-Simple = 3.05
Obsoletes: perl-Pod-Simple < 3.05
Conflicts: perl-Parse-RecDescent < 1.80-6mdk
Conflicts: perl-Filter < 1.28-6mdk
Conflicts: apache-mod_perl <= 1.3.24_1.26-1mdk
%define _requires_exceptions Mac\\|VMS\\|perl >=\\|perl(Errno)\\|perl(Fcntl)\\|perl(IO)\\|perl(IO::File)\\|perl(IO::Socket::INET)\\|perl(IO::Socket::UNIX)\\|perl(Tk)\\|perl(Tk::Pod)\\|perlapi-

# for NDBM
BuildRequires: db5-devel
BuildRequires: gdbm-devel
%if "%{_lib}" == "lib64"
BuildRequires: devel(libgdbm_compat(64bit))
%else
BuildRequires: devel(libgdbm_compat)
%endif
# we need >= 1.129 to get perl(abi) deps
BuildRequires: rpm-mandriva-setup-build >= 1.129

BuildRequires: man

%package base
Version:  %{version}
Summary:  The Perl programming language (base)
Provides: perl(v5.6.0) perl(base) perl(bytes) perl(constant) perl(integer) perl(lib) perl(overload) perl(strict) perl(utf8) perl(vars) perl(warnings) perl(Carp::Heavy)
Group:    Development/Perl
Url:      http://www.perl.org/
# notice that theese are only kept for backwards compatibility, from now
# on a perl(abi) = <version> will automatically be added by the dep generator
# and packages will depend on perl(abi) >= <version>
Provides: perlapi-5.12.0
Provides: perlapi-5.12.1
Provides: perlapi-5.12.2
Provides: perlapi-5.12.3
# explicit file provides
Provides: /usr/bin/perl
# MD perl binary is linked to libfreebl3.so which can be found in lib*nss3
# but there is no automatic linking done in the rpm itself
# this manual require can be removed if ever fixed
Requires: %{_lib}nss3
# perlapi-xxx didn't exist for 5.8.8, so we need to put the more important conflicts:
Conflicts: perl-URPM < 3.07-2
Conflicts: perl-RPM4 < 0.23-4
Conflicts: perl-Locale-gettext < 1.05-6
Conflicts: perl-Digest-SHA1 < 2.11-4
Conflicts: perl-Net-DBus < 0.33.5-2
Conflicts: perl-XML-Parser < 2.35
Conflicts: drakxtools-backend < 10.6.4
# perl-suid is gone is perl 5.12
Obsoletes: perl-suid

%package devel
Version:  %{version}
Summary:  The Perl programming language (devel)
Group:    Development/Perl
Url: http://www.perl.org/
# for each package linked against libperl.so, rpm will
# add an automatic dependency on devel(libperl) for
# the corresponding devel package, but rpm will not
# automatically provides it, as libperl.so is not in
# standard library path
%ifarch %ix86
Provides:   devel(libperl)
%endif
%ifarch x86_64
Provides:   devel(libperl(64bit))
%endif
Requires: %{name} = %{epoch}:%{version}-%{release}

%package doc
Version:  %{version}
Summary:  The Perl programming language (documentation)
Group:    Development/Perl
Url:      http://www.perl.org/
BuildArch:	noarch
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: groff-for-man
Requires: perl(Pod::Perldoc)

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

You need perl-base to have a full perl.

%description base
This is the base package for %{name}.

%description devel
This is the devel package for %{name}.

%description doc
This is the documentation package for %{name}.
It contains also the 'perldoc' program.

%prep
%setup -q -n %{name}-%{version}%{rel}
%patch6 -p0
%patch14 -p0
%patch15 -p1
%patch16 -p0
%patch21 -p1 -b .peroyvind
%patch23 -p0
%patch29 -p0
%patch32 -p1
%patch38 -p0
%patch43 -p0
%patch44 -p0
%patch48 -p0
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1

%patch65 -p1

remove_from_lists() {
    perl -ni -e "m!^\Q$1! or print" MANIFEST
    perl -ni -e "m!^\Q$1! or print" utils.lst
}
remove_files() {
    rm -r $1
    remove_from_lists $1
}
remove_files_all() {
    rm -r $1*
    remove_from_lists $1
}
remove_util() {
    perl -pi -e "/^pl(extract)?\s/ and s/\s$1\b//" utils/Makefile.SH
}

chmod u+w -R *
# perl-Archive-Tar
remove_files cpan/Archive-Tar/
remove_files_all utils/ptar.PL
remove_files_all utils/ptardiff.PL
remove_util ptar
remove_util ptardiff
# perl-Digest-SHA
remove_files cpan/Digest-SHA/
remove_files_all utils/shasum
remove_util shasum
# perl-CPANPLUS
remove_files cpan/CPANPLUS/
remove_files_all utils/cpan2dist.PL
remove_files_all utils/cpanp-run-perl.PL
remove_files_all utils/cpanp.PL
remove_util cpan2dist
remove_util cpanp-run-perl
remove_util cpanp
# perl-CPANPLUS-Dist-Build
remove_files cpan/CPANPLUS-Dist-Build/
# perl-Module-CoreList
remove_files dist/Module-CoreList/
remove_files_all utils/corelist.PL
remove_util corelist
# perl-Module-Build
remove_files cpan/Module-Build/
remove_files_all utils/config_data.PL
remove_util config_data
# perl-CGI
remove_files cpan/CGI/
# perl-Archive-Extract
remove_files cpan/Archive-Extract/
# perl-Time-Piece
remove_files cpan/Time-Piece/
# perl-Pod-Perldoc
remove_files dist/Pod-Perldoc/
remove_files_all utils/perldoc.PL
remove_util perldoc

%build
%ifarch ppc
   RPM_OPT_FLAGS=`echo "$RPM_OPT_FLAGS"|sed -e 's/-O2/-O1/g'`
%endif

sh Configure -des \
  -Dinc_version_list="5.12.2 5.12.2/%{full_arch} 5.12.1 5.12.1/%{full_arch} 5.12.0 5.12.0/%{full_arch} 5.10.1 5.10.0 5.8.8 5.8.7 5.8.6 5.8.5 5.8.4 5.8.3 5.8.2 5.8.1 5.8.0 5.6.1 5.6.0" \
  -Darchname=%{arch}-%{_os} \
  -Dcc='%{__cc}' \
%if %debugging
  -Doptimize=-g -DDEBUGGING \
%else
  -Doptimize="$RPM_OPT_FLAGS" -DDEBUGGING=-g \
%endif
  -Dccflags="%{optflags} -fno-strict-aliasing" \
  -Dccdlflags="%{ldflags} -Wl,-rpath=%{perl_root}/%{version}/%{full_arch}/CORE" \
  -Dldflags="%{ldflags} -Wl,-rpath=%{perl_root}/%{version}/%{full_arch}/CORE" \
  -Dcppflags="-D_REENTRANT -D_GNU_SOURCE" \
  -Dlibpth='' \
  -Dprefix=%_prefix -Dvendorprefix=%_prefix \
  -Dsiteprefix=%_prefix -Dsitebin=%_prefix/local/bin \
  -Dsiteman1dir=%_prefix/local/share/man/man1 \
  -Dsiteman3dir=%_prefix/local/share/man/man3 \
  -Dman3dir=%_mandir/man3pm \
  -Dvendorman3dir=%_mandir/man3 \
  -Dman3ext=3pm \
  -Dcf_by=Mandriva -Dmyhostname=localhost -Dperladmin=root@localhost -Dcf_email=root@localhost  \
  -Ud_csh \
  -Duseshrplib \
%if %threading
  -Duseithreads \
%endif
%ifarch %{sparc}
  -Ud_longdbl \
%endif
  -Di_db \
  -Di_ndbm \
  -Di_gdbm \

%make

%check
# for test, building a perl with no rpath
# for test, unset RPM_BUILD_ROOT so that the MakeMaker trick is not triggered
rm -f perl
%define nbprocs %(/usr/bin/getconf _NPROCESSORS_ONLN)
RPM_BUILD_ROOT="" TEST_JOBS=%{nbprocs} make test_harness_notty CCDLFLAGS=
rm -f perl
make perl

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

install -d $RPM_BUILD_ROOT%{perl_root}/vendor_perl/%{version}/%{full_arch}/auto

# We prefer 0755 instead of 0555
find $RPM_BUILD_ROOT -name "*.so" | xargs chmod 0755

cp -f utils/h2ph utils/h2ph_patched
cat %{SOURCE2} | patch -p1

# LD_PRELOAD doesn't work... why?
LD_LIBRARY_PATH=`pwd` ./perl -Ilib utils/h2ph_patched -a -d $RPM_BUILD_ROOT%{perl_root}/%{version}/%{full_arch} `cat %{SOURCE1}` > /dev/null ||:

(
    # i don't like hardlinks, having symlinks instead:
    cd $RPM_BUILD_ROOT%{_bindir}
    ln -sf perl5 perl
    ln -s perl%{version} perl5
)

rm -f $RPM_BUILD_ROOT%{_bindir}/perlivp $RPM_BUILD_ROOT%{_mandir}/man1/perlivp.1

%ifarch ppc
perl -ni -e 'print if !/sub __syscall_nr/' $RPM_BUILD_ROOT%{perl_root}/%{version}/%{full_arch}/asm/unistd.ph
%endif

%ifarch ppc
perl -ni -e 'print unless m/sub __syscall_nr/' $RPM_BUILD_ROOT/%{perl_root}/%{version}/%{full_arch}/asm/unistd.ph
%endif

# call spec-helper before creating the file list
# (spec-helper removes some files, and compress some others)
%define dont_strip 1
%{?__spec_helper_post}
%undefine dont_strip

(
   cat > perl-base.list <<EOF
%{_bindir}/perl
%{_bindir}/perl5
%{_bindir}/perl%{version}
%dir %{perl_root}
%dir %{perl_root}/%{version}
%dir %{perl_root}/%{version}/File
%{perl_root}/%{version}/File/Basename.pm
%{perl_root}/%{version}/File/Find.pm
%{perl_root}/%{version}/File/Path.pm
%dir %{perl_root}/%{version}/Getopt
%{perl_root}/%{version}/Getopt/Long.pm
%{perl_root}/%{version}/Getopt/Std.pm
%dir %{perl_root}/%{version}/Time
%{perl_root}/%{version}/Time/Local.pm
%{perl_root}/%{version}/AutoLoader.pm
%dir %{perl_root}/%{version}/Carp
%{perl_root}/%{version}/Carp.pm
%{perl_root}/%{version}/Carp/Heavy.pm
%{perl_root}/%{version}/DirHandle.pm
%{perl_root}/%{version}/%{full_arch}/Errno.pm
%dir %{perl_root}/%{version}/Exporter
%{perl_root}/%{version}/Exporter/Heavy.pm
%{perl_root}/%{version}/Exporter.pm
%{perl_root}/%{version}/FileHandle.pm
%{perl_root}/%{version}/PerlIO.pm
%{perl_root}/%{version}/SelectSaver.pm
%{perl_root}/%{version}/Symbol.pm
%dir %{perl_root}/%{version}/Tie
%{perl_root}/%{version}/Tie/Hash.pm
%{perl_root}/%{version}/XSLoader.pm
%{perl_root}/%{version}/base.pm
%{perl_root}/%{version}/bytes.pm
%{perl_root}/%{version}/bytes_heavy.pl
%{perl_root}/%{version}/constant.pm
%{perl_root}/%{version}/feature.pm
%{perl_root}/%{version}/integer.pm
%{perl_root}/%{version}/overload.pm
%{perl_root}/%{version}/strict.pm
%{perl_root}/%{version}/utf8.pm
%{perl_root}/%{version}/utf8_heavy.pl
%dir %{perl_root}/%{version}/unicore
%dir %{perl_root}/%{version}/unicore/To
%{perl_root}/%{version}/unicore/To/Lower.pl
%{perl_root}/%{version}/unicore/To/Fold.pl
%{perl_root}/%{version}/unicore/To/Upper.pl
%{perl_root}/%{version}/vars.pm
%dir %{perl_root}/%{version}/warnings
%{perl_root}/%{version}/warnings/register.pm
%{perl_root}/%{version}/warnings.pm
%dir %{perl_root}/%{version}/%{full_arch}
%{perl_root}/%{version}/%{full_arch}/lib.pm
%{perl_root}/%{version}/%{full_arch}/Cwd.pm
%dir %{perl_root}/%{version}/%{full_arch}/File
%{perl_root}/%{version}/%{full_arch}/File/Spec.pm
%{perl_root}/%{version}/%{full_arch}/File/Spec/Unix.pm
%dir %{perl_root}/%{version}/%{full_arch}/File/Spec
%{perl_root}/%{version}/%{full_arch}/Fcntl.pm
%{perl_root}/%{version}/%{full_arch}/IO.pm
%dir %{perl_root}/%{version}/%{full_arch}/IO
%{perl_root}/%{version}/%{full_arch}/IO/File.pm
%{perl_root}/%{version}/%{full_arch}/IO/Handle.pm
%{perl_root}/%{version}/%{full_arch}/IO/Seekable.pm
%{perl_root}/%{version}/%{full_arch}/IO/Select.pm
%{perl_root}/%{version}/%{full_arch}/IO/Socket.pm
%dir %{perl_root}/%{version}/%{full_arch}/auto
%dir %{perl_root}/%{version}/%{full_arch}/auto/Cwd
%{perl_root}/%{version}/%{full_arch}/auto/Cwd/Cwd.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/DynaLoader
%{perl_root}/%{version}/%{full_arch}/auto/DynaLoader/dl_findfile.al
%dir %{perl_root}/%{version}/%{full_arch}/auto/Data
%dir %{perl_root}/%{version}/%{full_arch}/auto/Data/Dumper
%{perl_root}/%{version}/%{full_arch}/auto/Data/Dumper/Dumper.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Fcntl
%{perl_root}/%{version}/%{full_arch}/auto/Fcntl/Fcntl.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/File
%dir %{perl_root}/%{version}/%{full_arch}/auto/File/Glob
%{perl_root}/%{version}/%{full_arch}/auto/File/Glob/Glob.so
%{perl_root}/%{version}/%{full_arch}/File/Glob.pm
%dir %{perl_root}/%{version}/%{full_arch}/auto/IO
%{perl_root}/%{version}/%{full_arch}/auto/IO/IO.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/POSIX
%{perl_root}/%{version}/%{full_arch}/auto/POSIX/POSIX.so
%{perl_root}/%{version}/%{full_arch}/auto/POSIX/autosplit.ix
%{perl_root}/%{version}/%{full_arch}/auto/POSIX/load_imports.al
%{perl_root}/%{version}/%{full_arch}/auto/POSIX/tmpfile.al
%dir %{perl_root}/%{version}/%{full_arch}/auto/Socket
%{perl_root}/%{version}/%{full_arch}/auto/Socket/Socket.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Storable
%{perl_root}/%{version}/%{full_arch}/auto/Storable/Storable.so
%{perl_root}/%{version}/%{full_arch}/auto/Storable/autosplit.ix
%{perl_root}/%{version}/%{full_arch}/auto/Storable/store.al
%{perl_root}/%{version}/%{full_arch}/auto/Storable/_store.al
%{perl_root}/%{version}/%{full_arch}/auto/Storable/retrieve.al
%{perl_root}/%{version}/%{full_arch}/auto/Storable/_retrieve.al
%dir %{perl_root}/%{version}/%{full_arch}/auto/re
%{perl_root}/%{version}/%{full_arch}/auto/re/re.so
%{perl_root}/%{version}/%{full_arch}/Config.pm
%{perl_root}/%{version}/%{full_arch}/Config_heavy.pl
%{perl_root}/%{version}/%{full_arch}/DynaLoader.pm
%{perl_root}/%{version}/%{full_arch}/POSIX.pm
%{perl_root}/%{version}/%{full_arch}/Socket.pm
%{perl_root}/%{version}/%{full_arch}/Storable.pm
%{perl_root}/%{version}/%{full_arch}/re.pm
%dir %{perl_root}/%{version}/%{full_arch}/CORE
%{perl_root}/%{version}/%{full_arch}/CORE/libperl.so
%dir %{perl_root}/%{version}/%{full_arch}/asm
%dir %{perl_root}/%{version}/%{full_arch}/bits
%dir %{perl_root}/%{version}/%{full_arch}/sys
%{perl_root}/%{version}/%{full_arch}/asm/unistd.ph
%ifarch %mips
%{perl_root}/%{version}/%{full_arch}/asm/sgidefs.ph
%endif
%ifarch ia64
%{perl_root}/%{version}/%{full_arch}/asm/break.ph
%endif
%ifarch x86_64
%{perl_root}/%{version}/%{full_arch}/bits/wordsize.ph
%endif
%ifarch %ix86 x86_64
%{perl_root}/%{version}/%{full_arch}/asm/unistd_32.ph
%{perl_root}/%{version}/%{full_arch}/asm/unistd_64.ph
%endif
%ifarch ppc64
%{perl_root}/%{version}/%{full_arch}/asm-ppc/unistd.ph
%{perl_root}/%{version}/%{full_arch}/asm-ppc64/unistd.ph
%{perl_root}/%{version}/%{full_arch}/bits/wordsize.ph
%endif
%{perl_root}/%{version}/%{full_arch}/bits/syscall.ph
%{perl_root}/%{version}/%{full_arch}/sys/syscall.ph
%{perl_root}/%{version}/%{full_arch}/_h2ph_pre.ph
%{perl_root}/%{version}/%{full_arch}/syscall.ph
EOF

   cat > perl.list <<EOF
%doc README
%doc Artistic
%{_bindir}/a2p
%{_bindir}/perlbug
%{_bindir}/perlthanks
%{_bindir}/find2perl
%{_bindir}/pod2man
%{_bindir}/pod2html
%{_bindir}/pod2text
%{_bindir}/pod2latex
%{_bindir}/splain
%{_bindir}/s2p
EOF

   cat > perl-devel.list <<EOF
%{_bindir}/cpan
%{_bindir}/pstruct
%{_bindir}/piconv
%{_bindir}/dprofpp
%{_bindir}/c2ph
%{_bindir}/h2xs
%{_bindir}/enc2xs
%{_bindir}/instmodsh
%{_bindir}/libnetcfg
%{_bindir}/h2ph
%{_bindir}/pl2pm
%{_bindir}/podchecker
%{_bindir}/podselect
%{_bindir}/pod2usage
%{_bindir}/psed
%{_bindir}/prove
%{_bindir}/xsubpp
%{perl_root}/%{version}/Encode/encode.h
%{perl_root}/%{version}/%{full_arch}/CORE/EXTERN.h
%{perl_root}/%{version}/%{full_arch}/CORE/INTERN.h
%{perl_root}/%{version}/%{full_arch}/CORE/XSUB.h
%{perl_root}/%{version}/%{full_arch}/CORE/av.h
%{perl_root}/%{version}/%{full_arch}/CORE/cc_runtime.h
%{perl_root}/%{version}/%{full_arch}/CORE/cop.h
%{perl_root}/%{version}/%{full_arch}/CORE/cv.h
%{perl_root}/%{version}/%{full_arch}/CORE/dosish.h
%{perl_root}/%{version}/%{full_arch}/CORE/embed.h
%{perl_root}/%{version}/%{full_arch}/CORE/embedvar.h
%{perl_root}/%{version}/%{full_arch}/CORE/fakesdio.h
%{perl_root}/%{version}/%{full_arch}/CORE/fakethr.h
%{perl_root}/%{version}/%{full_arch}/CORE/form.h
%{perl_root}/%{version}/%{full_arch}/CORE/gv.h
%{perl_root}/%{version}/%{full_arch}/CORE/handy.h
%{perl_root}/%{version}/%{full_arch}/CORE/hv.h
%{perl_root}/%{version}/%{full_arch}/CORE/intrpvar.h
%{perl_root}/%{version}/%{full_arch}/CORE/iperlsys.h
%{perl_root}/%{version}/%{full_arch}/CORE/keywords.h
%{perl_root}/%{version}/%{full_arch}/CORE/malloc_ctl.h
%{perl_root}/%{version}/%{full_arch}/CORE/mg.h
%{perl_root}/%{version}/%{full_arch}/CORE/nostdio.h
%{perl_root}/%{version}/%{full_arch}/CORE/op.h
%{perl_root}/%{version}/%{full_arch}/CORE/opcode.h
%{perl_root}/%{version}/%{full_arch}/CORE/opnames.h
%{perl_root}/%{version}/%{full_arch}/CORE/overload.h
%{perl_root}/%{version}/%{full_arch}/CORE/pad.h
%{perl_root}/%{version}/%{full_arch}/CORE/parser.h
%{perl_root}/%{version}/%{full_arch}/CORE/patchlevel.h
%{perl_root}/%{version}/%{full_arch}/CORE/perlapi.h
%{perl_root}/%{version}/%{full_arch}/CORE/perlio.h
%{perl_root}/%{version}/%{full_arch}/CORE/perliol.h
%{perl_root}/%{version}/%{full_arch}/CORE/perlsdio.h
%{perl_root}/%{version}/%{full_arch}/CORE/perlsfio.h
%{perl_root}/%{version}/%{full_arch}/CORE/perlvars.h
%{perl_root}/%{version}/%{full_arch}/CORE/perly.h
%{perl_root}/%{version}/%{full_arch}/CORE/pp.h
%{perl_root}/%{version}/%{full_arch}/CORE/pp_proto.h
%{perl_root}/%{version}/%{full_arch}/CORE/proto.h
%{perl_root}/%{version}/%{full_arch}/CORE/reentr.h
%{perl_root}/%{version}/%{full_arch}/CORE/regcharclass.h
%{perl_root}/%{version}/%{full_arch}/CORE/regcomp.h
%{perl_root}/%{version}/%{full_arch}/CORE/regexp.h
%{perl_root}/%{version}/%{full_arch}/CORE/regnodes.h
%{perl_root}/%{version}/%{full_arch}/CORE/scope.h
%{perl_root}/%{version}/%{full_arch}/CORE/sv.h
%{perl_root}/%{version}/%{full_arch}/CORE/thread.h
%{perl_root}/%{version}/%{full_arch}/CORE/uconfig.h
%{perl_root}/%{version}/%{full_arch}/CORE/unixish.h
%{perl_root}/%{version}/%{full_arch}/CORE/utf8.h
%{perl_root}/%{version}/%{full_arch}/CORE/utfebcdic.h
%{perl_root}/%{version}/%{full_arch}/CORE/util.h
%{perl_root}/%{version}/%{full_arch}/CORE/uudmap.h
%{perl_root}/%{version}/%{full_arch}/CORE/warnings.h
EOF

   rel_perl_root=`echo %{perl_root} | sed "s,/,,"`
   rel_mandir=`echo %{_mandir} | sed "s,/,,"`
   (cd $RPM_BUILD_ROOT ; find $rel_perl_root/%{version} "(" -name "*.pod" -o -iname "Changes*" -o -iname "ChangeLog*" -o -iname "README*" ")" -a -not -name perldiag.pod -printf "%%%%doc /%%p\n") >> perl-doc-dupes.list
   sort -u perl-doc-dupes.list -o perl-doc.list
   (cd $RPM_BUILD_ROOT ; find $rel_mandir/man1 ! -name "perlivp.1*" ! -type d -printf "/%%p\n") >> perl.list
   (cd $RPM_BUILD_ROOT ; find $rel_mandir/man3pm ! -type d ! -name "Pod::Perldoc*" -printf "/%%p\n") >> perl.list
   (cd $RPM_BUILD_ROOT ; find $rel_perl_root/%{version} ! -type d -printf "/%%p\n") >> perl.list
   (cd $RPM_BUILD_ROOT ; find $rel_perl_root/%{version} -type d -printf "%%%%dir /%%p\n") >> perl.list

   perl -ni -e 'BEGIN { open F, "perl-base.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' perl.list
   perl -ni -e 'BEGIN { open F, "perl-devel.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' perl.list
   perl -ni -e 'BEGIN { open F, "perl-doc.list"; s/^.doc //, $s{$_} = 1 foreach <F>; } print unless $s{$_}' perl.list
)

%clean
rm -rf $RPM_BUILD_ROOT

%files -f perl.list
%defattr(-,root,root)

%files base -f perl-base.list
%defattr(-,root,root)

%files devel -f perl-devel.list
%defattr(-,root,root)

%files doc -f perl-doc.list
%defattr(-,root,root)
