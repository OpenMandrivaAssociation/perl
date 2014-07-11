%define threading 1
%define debugging 0

%if %{threading}
%define thread_arch -thread-multi
%endif

%define full_arch %{_arch}-%{_os}%{?thread_arch}
# Don't change to %{_libdir} as perl is clean and has arch-dependent subdirs
%define perl_root %{_prefix}/lib/perl5

%define	major	5.16
%define	libname	%mklibname perl %{major}

Summary:	The Perl programming language
Name:		perl
Epoch:		2
Version:	%{major}.3
Release:	12
License:	GPL+ or Artistic
Group:		Development/Perl
Url:		http://www.perl.org/
# ftp://ftp.funet.fi/pub/languages/perl/snap/perl@17574.tbz
#ftp://ftp.funet.fi/pub/languages/perl/CPAN/src/perl-%{version}.tar.bz2
Source0:	http://www.cpan.org/src/%{name}-%{version}.tar.gz
Source1:	perl-headers-wanted
Source2:	perl-5.8.0-RC2-special-h2ph-not-failing-on-machine_ansi_header.patch
Patch5:		perl-5.14.0-fix_eumm_append_to_config_cflags_instead_of_overriding.patch
Patch6:		perl-5.16.0-fix-LD_RUN_PATH-for-MakeMaker.patch
Patch14:	perl-5.12.0-RC0-install-files-using-chmod-644.patch
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
Patch51:	perl-5.16.2-add-soname-to-libperl.patch
#
# fixes taken from debian
#
# Fix a segmentation fault occurring in the mod_perl2 test suite (debian #475498, perl #33807)
Patch65:	local_symtab.diff
Patch66:	perl-5.14.2-USE_MM_LD_RUN_PATH.patch
Patch67:	perl-5.16.0-update-sha1sum-used-in-testsuite.patch
# (tpg)https://rt.perl.org/Public/Bug/Display.html?id=121505
# gcc 4.9 by default does some optimizations that break perl
# add -fwrapv to ccflags
Patch68:	0001-perl-121505-add-fwrapv-to-ccflags-for-gcc-4.9-and-la.patch

# for NDBM
BuildRequires:	db5-devel
BuildRequires:	gdbm-devel
BuildRequires:	man
Requires:	perl-base = %{EVRD}

# the following modules are part of perl normally, but are shipped in
# separated rpm packages. let's require them in order to please people
# that think that installing "perl" will have a full perl as shipped by
# upstream. (cf tom christiansen and the lengthy thread:
# http://www.nntp.perl.org/group/perl.perl5.porters/2009/08/msg149747.html)
Suggests:	perl(Archive::Extract)
Suggests:	perl(Archive::Tar)
Suggests:	perl(CGI)
Suggests:	perl(Compress::Raw::Bzip2)
Suggests:	perl(Compress::Raw::Zlib)
Suggests:	perl(Compress::Zlib)
Suggests:	perl(CPANPLUS)
Suggests:	perl(CPANPLUS::Dist::Build)
Suggests:	perl(Digest::SHA)
Suggests:	perl(IO::Compress::Bzip2)
Requires:	perl(JSON::PP)
Suggests:	perl(Module::Build)
Suggests:	perl(Module::CoreList)
Suggests:	perl(Pod::Perldoc)
Suggests:	perl(Time::Piece)

# Used to be maintained separately, bundled now
Provides:	perl-CPAN-Meta-YAML = 0.007
Obsoletes:	perl-CPAN-Meta-YAML < 0.007
Provides:	perl-MIME-Base64 = 3.080.0
Provides:	perl-libnet
Provides:	perl-Storable = 2.200.0
Provides:	perl-Digest-MD5 = 2.390.0
Provides:	perl-Time-HiRes = 1:1.971.900
Provides:	perl-Locale-Codes
Provides:	perl-Test-Simple = 0.920.0
Provides:	perl-Test-Builder-Tester = 1.180.0
Provides:	perl(version) = 1:0.74
Provides:	perl-version = 1:0.74
Provides:	perl-File-Fetch = 0.14
Provides:	perl-CPAN = 1.9205
Provides:	perl-IO-Zlib = 1.07
Provides:	perl-Pod-Simple = 3.05
%define __noautoreq '(Mac|VMS|perl\\(Errno\\)|perl\\(Fcntl\\)|perl\\(IO\\)|perl\\(IO::File\\)|perl\\(IO::Socket::INET\\)|perl\\(IO::Socket::UNIX\\)|perl\\(Tk\\)|perl\\(Tk::Pod\\))'

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

%package	base
Summary:	The Perl programming language (base)
Group:		Development/Perl
Provides:	perl(base)
Provides:	perl(Carp::Heavy)
Provides:	perl(constant)
Provides:	perl(integer)
Provides:	perl(overload)
Provides:	perl(strict)
Provides:	perl(utf8)
Provides:	perl(vars)
Provides:	perl(warnings)
# explicit file provides
Provides:	/usr/bin/perl
# perl-suid is gone is perl 5.12
Obsoletes:	perl-suid
Requires:	%{libname} = %{EVRD}

%description	base
This is the base package for %{name}.

%package -n	%{libname}
Summary:	Shared library for perl
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared library for perl.

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
%patch14 -p0
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
%patch67 -p1 -b .sha1sum~
%patch68 -p1 -b .fwrapv~

# fix linking against libperl during build
ln -s $PWD lib/CORE

%build
%ifarch aarch64
export AFLAGS="-Wl,--hash-style=both"
%endif
sh Configure -des \
  -Dinc_version_list="5.16.2 5.16.2/%{full_arch} 5.16.1 5.16.1/%{full_arch} 5.16.0 5.16.0/%{full_arch} 5.14.2 5.14.1 5.14.0 5.12.3 5.12.2 5.12.1 5.12.0" \
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
%make

%check
# This test relies on Digest::SHA being available
rm -f t/porting/regen.t
sed -i -e '/^t\/porting\/regen.t/d' MANIFEST

# FIXME: should pick up library path automatically in patch..
export LIBRARY_PATH="$PWD"
TEST_JOBS=%(/usr/bin/getconf _NPROCESSORS_ONLN) make test_harness_notty CCDLFLAGS=

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

# Archive::Extract
rm -r	%{buildroot}%{perl_root}/%{version}/Archive/Extract.pm \
	%{buildroot}%{_mandir}/man3pm/Archive::Extract.3*

# idem CPANPLUS
rm -r	%{buildroot}%{_bindir}/cpan2dist \
	%{buildroot}%{_bindir}/cpanp \
	%{buildroot}%{_bindir}/cpanp-run-perl \
	%{buildroot}%{perl_root}/%{version}/CPANPLUS/ \
	%{buildroot}%{_mandir}/man1/cpan2dist.1* \
	%{buildroot}%{_mandir}/man1/cpanp.1* \
	%{buildroot}%{_mandir}/man3pm/CPANPLUS*

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

# Term::UI
rm -r	%{buildroot}%{perl_root}/%{version}/Term/UI.pm \
	%{buildroot}%{perl_root}/%{version}/Term/UI/ \
	%{buildroot}%{_mandir}/man3pm/Term::UI*

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

# Module::CoreList
rm -r	%{buildroot}%{_bindir}/corelist \
	%{buildroot}%{perl_root}/%{version}/Module/CoreList.pm \
	%{buildroot}%{_mandir}/man1/corelist* \
	%{buildroot}%{_mandir}/man3pm/Module::CoreList*

# call spec-helper before creating the file list
# (spec-helper removes some files, and compress some others)
%define dont_strip 1
%{?__spec_helper_post}
%undefine dont_strip

cat > perl-base.list <<EOF
%{_bindir}/perl
%{_bindir}/perl5
%{_bindir}/perl%{version}
%dir %{_mandir}/man3pm
%dir %{perl_root}
%dir %{perl_root}/%{version}
%dir %{perl_root}/%{version}/File
%{perl_root}/%{version}/autouse.pm
%{perl_root}/%{version}/AnyDBM_File.pm
%{perl_root}/%{version}/FindBin.pm
%{perl_root}/%{version}/File/Basename.pm
%{perl_root}/%{version}/File/Find.pm
%{perl_root}/%{version}/File/Path.pm
%{perl_root}/%{version}/File/Temp.pm
%dir %{perl_root}/%{version}/Getopt
%{perl_root}/%{version}/Getopt/Long.pm
%{perl_root}/%{version}/Getopt/Std.pm
%dir %{perl_root}/%{version}/Encode
%{perl_root}/%{version}/Encode/ConfigLocal_PM.e2x
%{perl_root}/%{version}/Encode/Makefile_PL.e2x
%{perl_root}/%{version}/Encode/_PM.e2x
%{perl_root}/%{version}/Encode/_T.e2x
%dir %{perl_root}/%{version}/Net
%{perl_root}/%{version}/Net/Cmd.pm
%{perl_root}/%{version}/Net/Config.pm
%dir %{perl_root}/%{version}/Net/FTP
%{perl_root}/%{version}/Net/FTP.pm
%{perl_root}/%{version}/Net/FTP/A.pm
%{perl_root}/%{version}/Net/FTP/E.pm
%{perl_root}/%{version}/Net/FTP/I.pm
%{perl_root}/%{version}/Net/FTP/L.pm
%{perl_root}/%{version}/Net/FTP/dataconn.pm

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
%{perl_root}/%{version}/%{full_arch}/B.pm
%dir %{perl_root}/%{version}/%{full_arch}/auto/B
%{perl_root}/%{version}/%{full_arch}/auto/B/B.so
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
%dir %{perl_root}/%{version}/%{full_arch}/IO/Socket
%{perl_root}/%{version}/%{full_arch}/IO/Socket/INET.pm
%dir %{perl_root}/%{version}/%{full_arch}/auto
%dir %{perl_root}/%{version}/%{full_arch}/auto/Cwd
%{perl_root}/%{version}/%{full_arch}/auto/Cwd/Cwd.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Data
%dir %{perl_root}/%{version}/%{full_arch}/auto/Data/Dumper
%{perl_root}/%{version}/%{full_arch}/auto/Data/Dumper/Dumper.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Fcntl
%{perl_root}/%{version}/%{full_arch}/auto/Fcntl/Fcntl.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/File
%dir %{perl_root}/%{version}/%{full_arch}/auto/File/Glob
%{perl_root}/%{version}/%{full_arch}/auto/File/Glob/Glob.so
%{perl_root}/%{version}/%{full_arch}/File/Glob.pm
%dir %{perl_root}/%{version}/%{full_arch}/auto/MIME
%dir %{perl_root}/%{version}/%{full_arch}/auto/MIME/Base64
%{perl_root}/%{version}/%{full_arch}/auto/MIME/Base64/Base64.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Digest
%dir %{perl_root}/%{version}/%{full_arch}/auto/Digest/MD5
%{perl_root}/%{version}/%{full_arch}/auto/Digest/MD5/MD5.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/I18N
%dir %{perl_root}/%{version}/%{full_arch}/auto/I18N/Langinfo/
%{perl_root}/%{version}/%{full_arch}/auto/I18N/Langinfo/Langinfo.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/IO
%{perl_root}/%{version}/%{full_arch}/auto/IO/IO.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Encode
%{perl_root}/%{version}/%{full_arch}/Encode.pm
%{perl_root}/%{version}/%{full_arch}/Encode/Alias.pm
%{perl_root}/%{version}/%{full_arch}/Encode/Byte.pm
%{perl_root}/%{version}/%{full_arch}/Encode/CJKConstants.pm
%{perl_root}/%{version}/%{full_arch}/Encode/Config.pm
%{perl_root}/%{version}/%{full_arch}/Encode/EBCDIC.pm
%{perl_root}/%{version}/%{full_arch}/Encode/Encoder.pm
%{perl_root}/%{version}/%{full_arch}/Encode/Encoding.pm
%{perl_root}/%{version}/%{full_arch}/Encode/GSM0338.pm
%{perl_root}/%{version}/%{full_arch}/Encode/Guess.pm
%dir %{perl_root}/%{version}/%{full_arch}/Encode/MIME
%dir %{perl_root}/%{version}/%{full_arch}/Encode/MIME/Header
%{perl_root}/%{version}/%{full_arch}/Encode/MIME/Header.pm
%{perl_root}/%{version}/%{full_arch}/Encode/MIME/Header/ISO_2022_JP.pm
%{perl_root}/%{version}/%{full_arch}/Encode/MIME/Name.pm
%{perl_root}/%{version}/%{full_arch}/Encode/Symbol.pm
%dir %{perl_root}/%{version}/%{full_arch}/Encode/Unicode
%{perl_root}/%{version}/%{full_arch}/Encode/Unicode.pm
%{perl_root}/%{version}/%{full_arch}/Encode/Unicode/UTF7.pm
%dir %{perl_root}/%{version}/%{full_arch}/auto/Encode/Byte
%{perl_root}/%{version}/%{full_arch}/auto/Encode/Byte/Byte.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Encode/EBCDIC
%{perl_root}/%{version}/%{full_arch}/auto/Encode/EBCDIC/EBCDIC.so
%{perl_root}/%{version}/%{full_arch}/auto/Encode/Encode.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Encode/Symbol
%{perl_root}/%{version}/%{full_arch}/auto/Encode/Symbol/Symbol.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Encode/Unicode
%{perl_root}/%{version}/%{full_arch}/auto/Encode/Unicode/Unicode.so
%dir %{perl_root}/%{version}/%{full_arch}/List
%dir %{perl_root}/%{version}/%{full_arch}/List/Util
%{perl_root}/%{version}/%{full_arch}/List/Util.pm
%{perl_root}/%{version}/%{full_arch}/List/Util/XS.pm
%dir %{perl_root}/%{version}/%{full_arch}/auto/List
%dir %{perl_root}/%{version}/%{full_arch}/auto/List/Util
%{perl_root}/%{version}/%{full_arch}/auto/List/Util/Util.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/POSIX
%{perl_root}/%{version}/%{full_arch}/auto/POSIX/POSIX.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Socket
%{perl_root}/%{version}/%{full_arch}/auto/Socket/Socket.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Storable
%{perl_root}/%{version}/%{full_arch}/auto/Storable/Storable.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/re
%{perl_root}/%{version}/%{full_arch}/auto/re/re.so
%{perl_root}/%{version}/%{full_arch}/Config.pm
%{perl_root}/%{version}/%{full_arch}/Config_heavy.pl
%dir %{perl_root}/%{version}/%{full_arch}/Digest
%{perl_root}/%{version}/%{full_arch}/Digest/MD5.pm
%{perl_root}/%{version}/%{full_arch}/DynaLoader.pm
%dir %{perl_root}/%{version}/%{full_arch}/Encode
%dir %{perl_root}/%{version}/%{full_arch}/I18N
%{perl_root}/%{version}/%{full_arch}/I18N/Langinfo.pm
%dir %{perl_root}/%{version}/%{full_arch}/MIME
%{perl_root}/%{version}/%{full_arch}/MIME/Base64.pm
%{perl_root}/%{version}/%{full_arch}/MIME/QuotedPrint.pm
%{perl_root}/%{version}/%{full_arch}/POSIX.pm
%dir %{perl_root}/%{version}/%{full_arch}/Scalar/
%{perl_root}/%{version}/%{full_arch}/Scalar/Util.pm
%{perl_root}/%{version}/%{full_arch}/Socket.pm
%{perl_root}/%{version}/%{full_arch}/Storable.pm
%dir %{perl_root}/%{version}/%{full_arch}/Sys/
%dir %{perl_root}/%{version}/%{full_arch}/auto/Sys/
%dir %{perl_root}/%{version}/%{full_arch}/auto/Sys/Hostname
%{perl_root}/%{version}/%{full_arch}/Sys/Hostname.pm
%{perl_root}/%{version}/%{full_arch}/auto/Sys/Hostname/Hostname.so
%{perl_root}/%{version}/%{full_arch}/re.pm
%dir %{perl_root}/%{version}/%{full_arch}/CORE
%dir %{perl_root}/%{version}/%{full_arch}/asm
%dir %{perl_root}/%{version}/%{full_arch}/bits
%dir %{perl_root}/%{version}/%{full_arch}/sys
%{perl_root}/%{version}/%{full_arch}/asm/unistd.ph
%ifarch %{mipsx}
%{perl_root}/%{version}/%{full_arch}/asm/sgidefs.ph
%endif
%ifarch ia64
%{perl_root}/%{version}/%{full_arch}/asm/break.ph
%endif
%ifarch x86_64
%{perl_root}/%{version}/%{full_arch}/bits/wordsize.ph
%endif
%ifarch %{ix86} x86_64
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
%{_bindir}/prove
%{_bindir}/psed
%{_bindir}/pstruct
%{_bindir}/xsubpp
%{perl_root}/%{version}/Encode/encode.h
%{perl_root}/%{version}/%{full_arch}/CORE/*.h
%{_libdir}/libperl.so
EOF

cat > perl-doc.list <<EOF
#%{_bindir}/perldoc
#%{_mandir}/man3pm/Pod::Perldoc*
EOF

find %{buildroot}%{perl_root}/%{version} "(" -name "*.pod" -o -iname "Changes*" -o -iname "ChangeLog*" -o -iname "README*" ")" -a -not -name perldiag.pod -printf "%%%%doc %%p\n" |sort -u >> perl-doc.list
find %{buildroot}%{_mandir}/man1 ! -name "perlivp.1*" ! -type d >> perl.list
find %{buildroot}%{_mandir}/man3pm ! -type d ! -name "Pod::Perldoc*" >> perl.list
find %{buildroot}%{perl_root}/%{version} ! -type d ! -name \*.h >> perl.list
find %{buildroot}%{perl_root}/%{version} -type d -printf "%%%%dir %%p\n" >> perl.list
sed -e 's#%{buildroot}##g' -i perl*.list

perl -ni -e 'BEGIN { open F, "perl-base.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' perl.list
perl -ni -e 'BEGIN { open F, "perl-devel.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' perl.list
perl -ni -e 'BEGIN { open F, "perl-doc.list"; s/^.doc //, $s{$_} = 1 foreach <F>; } print unless $s{$_}' perl.list

%files -f perl.list

%files base -f perl-base.list

%files devel -f perl-devel.list

%files doc -f perl-doc.list

%files -n %{libname}
%{_libdir}/libperl.so.%{major}

