%define threading 1
%define debugging 0

%if %{threading}
%define thread_arch -thread-multi
%endif

%define full_arch %{_arch}-%{_os}%{?thread_arch}
# Don't change to %{_libdir} as perl is clean and has arch-dependent subdirs
%define perl_root %{_prefix}/lib/perl5

Name:		perl
%define	major	5.16
Version:	%{major}.2
Release:	3
Epoch:		2

Summary:	The Perl programming language
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
Patch50:	perl-5.14.2-link-perl-extensions-against-libperl.patch
Patch51:	perl-5.16.2-add-soname-to-libperl.patch
#
# fixes taken from debian
#
# Fix a segmentation fault occurring in the mod_perl2 test suite (debian #475498, perl #33807)
Patch65:	local_symtab.diff
Patch66:	perl-5.14.2-USE_MM_LD_RUN_PATH.patch
Patch67:	perl-5.16.0-update-sha1sum-used-in-testsuite.patch

Requires:	perl-base = %{EVRD}

# the following modules are dual-lifed modules, which are shipping
# scripts in /usr/bin. to prevent conflict, dual-lifed modules rename
# the scripts - but only after the listed version ;-)
Conflicts:	perl-Archive-Tar <= 1.840.0-4
Conflicts:	perl-CPANPLUS <= 0.910.500-5
Conflicts:	perl-Digest-SHA <= 5.620.0-5
Conflicts:	perl-JSON-PP <= 2.272.0-1
Conflicts:	perl-Module-Build <= 1:0.380.0-4
Conflicts:	perl-Module-CoreList <= 2.590.0-5
Conflicts:	perl-Pod-Perldoc <= 3.150.0-6
Conflicts:	perl-IO-Compress <= 2.49.0-1

# the following modules are part of perl normally, but are shipped in
# separated rpm packages. let's require them in order to please people
# that think that installing "perl" will have a full perl as shipped by
# upstream. (cf tom christiansen and the lengthy thread:
# http://www.nntp.perl.org/group/perl.perl5.porters/2009/08/msg149747.html)
Suggests:	perl-Archive-Extract
Suggests:	perl-Archive-Tar
Suggests:	perl-CGI
Suggests:	perl-CPANPLUS
Suggests:	perl-CPANPLUS-Dist-Build
Suggests:	perl-Digest-SHA
Suggests:	perl-Module-Build
Suggests:	perl-Module-CoreList
Suggests:	perl-Time-Piece

Provides:	perl-MIME-Base64 = 3.080.0
Obsoletes:	perl-MIME-Base64 < 3.080.0
Provides:	perl-libnet
Provides:	perl-Storable = 2.200.0
Obsoletes:	perl-Storable < 2.200.0
Provides:	perl-Digest-MD5 = 2.390.0
Obsoletes:	perl-Digest-MD5 < 2.390.0
Provides:	perl-Time-HiRes = 1:1.971.900
Obsoletes:	perl-Time-HiRes < 1:1.971.900
Provides:	perl-Locale-Codes
Provides:	perl-Test-Simple = 0.920.0
Obsoletes:	perl-Test-Simple < 0.920.0
Provides:	perl-Test-Builder-Tester = 1.180.0
Obsoletes:	perl-Test-Builder-Tester < 1.180.0

Provides:	perl(version) = 1:0.74
Provides:	perl-version = 1:0.74
Obsoletes:	perl-version < 1:0.74
Provides:	perl-File-Fetch = 0.14
Obsoletes:	perl-File-Fetch < 0.14
Provides:	perl-CPAN = 1.9205
Obsoletes:	perl-CPAN < 1.9205
Provides:	perl-IO-Zlib = 1.07
Obsoletes:	perl-IO-Zlib < 1.07
Provides:	perl-Pod-Simple = 3.05
Obsoletes:	perl-Pod-Simple < 3.05
Conflicts:	perl-Parse-RecDescent < 1.80-6mdk
Conflicts:	perl-Filter < 1.28-6mdk
Conflicts:	apache-mod_perl <= 1.3.24_1.26-1mdk
%define __noautoreq '(Mac|VMS|perl\\(Errno\\)|perl\\(Fcntl\\)|perl\\(IO\\)|perl\\(IO::File\\)|perl\\(IO::Socket::INET\\)|perl\\(IO::Socket::UNIX\\)|perl\\(Tk\\)|perl\\(Tk::Pod\\))'

# for NDBM
BuildRequires:	db5-devel
BuildRequires:	gdbm-devel

BuildRequires:	man

%package	base
Summary:	The Perl programming language (base)
Provides:	perl(base) perl(constant) perl(integer) perl(overload) perl(strict) perl(utf8) perl(vars) perl(warnings) perl(Carp::Heavy)
Group:		Development/Perl
Url:		http://www.perl.org/
# explicit file provides
Provides:	/usr/bin/perl
# perl-suid is gone is perl 5.12
Obsoletes:	perl-suid

%define	libname	%mklibname perl %{major}
%package -n	%{libname}
Summary:	Shared library for perl
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared library for perl.

%package	devel
Summary:	The Perl programming language (devel)
Group:		Development/Perl
Url:		http://www.perl.org/
Requires:	%{name} = %{EVRD}
# temporary dep due to the perl-5.14 bump
Requires:	perl-List-MoreUtils >= 0.320.0-4

%package	doc
Summary:	The Perl programming language (documentation)
Group:		Development/Perl
Url:		http://www.perl.org/
BuildArch:	noarch
Requires:	%{name} = %{EVRD}
Requires:	groff-for-man
Requires:	perl(Pod::Perldoc)

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

%description	base
This is the base package for %{name}.

%description	devel
This is the devel package for %{name}.

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

# fix linking against libperl during build
ln -s $PWD lib/CORE

%build
sh Configure -des \
  -Dinc_version_list="5.16.2 5.16.2/%{full_arch} 5.16.1 5.16.1/%{full_arch} 5.16.0 5.16.0/%{full_arch} 5.14.2 5.14.1 5.14.0 5.12.3 5.12.2 5.12.1 5.12.0" \
  -Darchname=%{_arch}-%{_os} \
  -Dcc='%{__cc}' \
%if %debugging
  -Doptimize="-O0" -DDEBUGGING="-g3 %{debugcflags}" \
%else
  -Doptimize="%{optflags}" -DDEBUGGING="%{debugcflags}" \
%endif
  -Dccdlflags="%{ldflags} -Wl,--warn-unresolved-symbols -fno-PIE" \
  -Dcccdlflags="-fPIC -fno-PIE" \
  -Dldflags="%{ldflags}" \
  -Dlddlflags="-shared %{optflags} %{ldflags} -Wl,--warn-unresolved-symbols -fno-PIE" \
  -Dcppflags="-D_REENTRANT -D_GNU_SOURCE" \
  -Dlibpth='%{_libdir} /%{_lib}' \
  -Dprefix=%{_prefix} -Dvendorprefix=%{_prefix} \
  -Dsiteprefix=%{_prefix} -Dsitebin=%{_prefix}/local/bin \
  -Dsiteman1dir=%{_prefix}/local/share/man/man1 \
  -Dsiteman3dir=%{_prefix}/local/share/man/man3 \
  -Dman3dir=%{_mandir}/man3pm \
  -Dvendorman3dir=%{_mandir}/man3 \
  -Dman3ext=3pm \
  -Dcf_by=%{vendor} -Dmyhostname=localhost -Dperladmin=root@localhost -Dcf_email=root@localhost \
  -Dperllibs='-lnsl -ldl -lm -lcrypt -lutil -lc -pthread'   \
  -Ud_csh \
  -Duseshrplib \
  -Duselargefiles \
  -Dpager='%{_bindir}/less -isr' \
%if %threading
  -Duseithreads \
%endif
%ifarch %{sparc}
  -Ud_longdbl \
%endif
  -Di_db \
  -Di_ndbm \
  -Di_gdbm
# workaround for not using colorgcc that relies on perl
PATH="${PATH#%{_datadir}/colorgcc:}"
%make

%check
# This test relies on Digest::SHA being available
rm -f t/porting/regen.t
sed -i -e '/^t\/porting\/regen.t/d' MANIFEST

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

# Get rid of stuff from Archive::Tar - the standalone package is released
# far more frequently
rm -rf	%buildroot%_bindir/ptar \
	%buildroot%_bindir/ptardiff \
	%buildroot%_bindir/ptargrep \
	%buildroot%perl_root/%version/Archive/Tar.pm \
	%buildroot%perl_root/%version/Archive/Tar

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
%{perl_root}/%{version}/File/GlobMapper.pm
%dir %{perl_root}/%{version}/Getopt
%{perl_root}/%{version}/Getopt/Long.pm
%{perl_root}/%{version}/Getopt/Std.pm
%dir %{perl_root}/%{version}/Encode
%{perl_root}/%{version}/Encode/ConfigLocal_PM.e2x
%{perl_root}/%{version}/Encode/Makefile_PL.e2x
%{perl_root}/%{version}/Encode/_PM.e2x
%{perl_root}/%{version}/Encode/_T.e2x
%dir %{perl_root}/%{version}/IO
%dir %{perl_root}/%{version}/Compress
%dir %{perl_root}/%{version}/IO/Compress
%{perl_root}/%{version}/Compress/Zlib.pm
%dir %{perl_root}/%{version}/IO/Compress/Adapter
%{perl_root}/%{version}/IO/Compress/Adapter/Bzip2.pm
%{perl_root}/%{version}/IO/Compress/Adapter/Deflate.pm
%{perl_root}/%{version}/IO/Compress/Adapter/Identity.pm
%dir %{perl_root}/%{version}/IO/Compress/Base
%{perl_root}/%{version}/IO/Compress/Base.pm
%{perl_root}/%{version}/IO/Compress/Base/Common.pm
%{perl_root}/%{version}/IO/Compress/Bzip2.pm
%{perl_root}/%{version}/IO/Compress/Deflate.pm
%dir %{perl_root}/%{version}/IO/Compress/Gzip
%{perl_root}/%{version}/IO/Compress/Gzip.pm
%{perl_root}/%{version}/IO/Compress/Gzip/Constants.pm
%{perl_root}/%{version}/IO/Compress/RawDeflate.pm
%dir %{perl_root}/%{version}/IO/Compress/Zip
%{perl_root}/%{version}/IO/Compress/Zip.pm
%{perl_root}/%{version}/IO/Compress/Zip/Constants.pm
%dir %{perl_root}/%{version}/IO/Compress/Zlib
%{perl_root}/%{version}/IO/Compress/Zlib/Constants.pm
%{perl_root}/%{version}/IO/Compress/Zlib/Extra.pm
%dir %{perl_root}/%{version}/IO/Uncompress
%dir %{perl_root}/%{version}/IO/Uncompress/Adapter
%{perl_root}/%{version}/IO/Uncompress/Adapter/Bunzip2.pm
%{perl_root}/%{version}/IO/Uncompress/Adapter/Identity.pm
%{perl_root}/%{version}/IO/Uncompress/Adapter/Inflate.pm
%{perl_root}/%{version}/IO/Uncompress/AnyInflate.pm
%{perl_root}/%{version}/IO/Uncompress/AnyUncompress.pm
%{perl_root}/%{version}/IO/Uncompress/Base.pm
%{perl_root}/%{version}/IO/Uncompress/Bunzip2.pm
%{perl_root}/%{version}/IO/Uncompress/Gunzip.pm
%{perl_root}/%{version}/IO/Uncompress/Inflate.pm
%{perl_root}/%{version}/IO/Uncompress/RawInflate.pm
%{perl_root}/%{version}/IO/Uncompress/Unzip.pm
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
%dir %{perl_root}/%{version}/%{full_arch}/Compress
%dir %{perl_root}/%{version}/%{full_arch}/Compress/Raw
%{perl_root}/%{version}/%{full_arch}/Compress/Raw/Bzip2.pm
%{perl_root}/%{version}/%{full_arch}/Compress/Raw/Zlib.pm
%dir %{perl_root}/%{version}/%{full_arch}/auto/Compress
%dir %{perl_root}/%{version}/%{full_arch}/auto/Compress/Raw
%dir %{perl_root}/%{version}/%{full_arch}/auto/Compress/Raw/Bzip2
%{perl_root}/%{version}/%{full_arch}/auto/Compress/Raw/Bzip2/Bzip2.so
%{perl_root}/%{version}/%{full_arch}/auto/Compress/Raw/Bzip2/autosplit.ix
%dir %{perl_root}/%{version}/%{full_arch}/auto/Compress/Raw/Zlib
%{perl_root}/%{version}/%{full_arch}/auto/Compress/Raw/Zlib/Zlib.so
%{perl_root}/%{version}/%{full_arch}/auto/Compress/Raw/Zlib/autosplit.ix
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
%{_bindir}/zipdetails
EOF

cat > perl-devel.list <<EOF
%{_bindir}/c2ph
%{_bindir}/config_data
%{_bindir}/corelist
%{_bindir}/cpan
%{_bindir}/cpan2dist
%{_bindir}/cpanp
%{_bindir}/cpanp-run-perl
%{_bindir}/enc2xs
%{_bindir}/h2ph
%{_bindir}/h2xs
%{_bindir}/instmodsh
%{_bindir}/json_pp
%{_bindir}/libnetcfg
%{_bindir}/piconv
%{_bindir}/pl2pm
%{_bindir}/pod2usage
%{_bindir}/podchecker
%{_bindir}/podselect
%{_bindir}/prove
%{_bindir}/psed
%{_bindir}/pstruct
%{_bindir}/shasum
%{_bindir}/xsubpp
%{perl_root}/%{version}/Encode/encode.h
%{perl_root}/%{version}/%{full_arch}/CORE/*.h
%{_libdir}/libperl.so
EOF

cat > perl-doc.list <<EOF
%{_bindir}/perldoc
%{_mandir}/man3pm/Pod::Perldoc*
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

%changelog
* Fri Dec 28 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.16.2-3
- pass '-lpthread' rather than '-pthread' to linker, otherwise it'll always
  link against libpthread, even when not needed

* Fri Dec 28 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.16.2-2
- link with '-lnsl -ldl -lm -lcrypt -lutil -lc -pthread' for modules by default

* Thu Dec 13 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.16.2-1
- make soname versioned and libify package (P51)
- update sha1sum in manifest used by test suite (P67)
- new version

* Tue Mar 13 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.14.2-6
+ Revision: 784543
- remove legacy external dependency filtering with internal dependency filtering
- don't add %%{_prefix}/local/%%{_lib} to library search dirs
- add soname to libperl.so (P51)
- link against libperl so that we reduce the number of unresolved symbols
  reported and also get automatic dependencies against it generated (P50)
- pass --warn-unresolved-symbols to linker so that we get warnings about
  unresolved symbols

* Thu Feb 23 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.14.2-5
+ Revision: 779342
- use %%mipsx to get all mips archs, rather than just %%mips
- use %%{EVRD} macro
- remove unused provides
- remove useless redefinitions of %%{version} per sub-package
- don't generate %%files manifests in subshells
- pass '-f' to rm when removing t/porting/regen.t in %%check to fix
  short-circuitability
- perl-base should own %%{_mandir}/man3pm
- be sure that all headers is packaged with -devel package
- clean up a bit with some cosmetics applied
- drop dead (and most likely no longer needed) ppc build workaround
- really pass %%ldflags to modules built

* Sun Feb 12 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.14.2-4
+ Revision: 773394
- don't generate LD_RUN_PATH for extensions by default (P66, from Fedora)
- set libpth properly in stead of what gets auto-detected by futile attempt of
  getting rid of LD_RUN_PATH being set when building extensions

* Thu Jan 26 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.14.2-3
+ Revision: 769194
- use %%{vendor} rather than hardcoding mandriva with -Dcf_by=
- fix passing of linker flags

* Mon Jan 23 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.14.2-2
+ Revision: 767213
- drop perlapi-<version> dependencies, 5.14.2 abi isn't backward compatible
- drop explicit perl(abi) provides

* Sat Jan 21 2012 Oden Eriksson <oeriksson@mandriva.com> 5.14.2-1.1
+ Revision: 763421
- add a temporary dep on perl-List-MoreUtils >= 0.320.0-4 in the perl-devel package instead of everywhere else, much faster...

* Thu Jan 19 2012 Bernhard Rosenkraenzer <bero@bero.eu> 5.14.2-1
+ Revision: 762564
- Append CFLAGS instead of overriding them
- Update to 5.14.2

* Thu Dec 01 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.12.3-11
+ Revision: 735903
- set -O0 for optimize for debug build
- use %%{debugcflags} for -DDEBUGGING, with -g3 added for debug build
- pass -Wl,--unresolved-symbols=ignore-all at end of linking perl extensions
  to override any possible --no-undefined being passed
- pass -fno-PIE to compiler flags when compiling perl extensions to avoid -fPIE
  sneakings it's way in and breaking build
- drop manual dependency on %%{_lib}nss3, glibc has the correct automatic
  dependency on it again now...

* Wed Nov 30 2011 Oden Eriksson <oeriksson@mandriva.com> 5.12.3-10
+ Revision: 735706
- let's see if it passes the tests in the build system...
- $$RPM_BUILD_ROOT is no more
- revert to what's in cooker

  + ZÃ© <ze@mandriva.org>
    - we need to avoid -Wl,--no-undefined
    - clean defattr
    - drop clean section (done by default)
    - we need to remove "-Wl,--no-undefined" to prevent breaks in apps that need perl

* Sat Sep 24 2011 Matthew Dawkins <mattydaw@mandriva.org> 5.12.3-9
+ Revision: 701186
- added manual requires for lib*nss3 for libfreebl3.so

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - enable -Ud_longdbl only for 32 bit %%{sparc}, not both 32 & 64 bit %%{sparcx}
    - try fix default perl build a bit
    - use %%{sparcx} macro rather than deprecated %%{sunsparc}

* Fri Jun 17 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.12.3-8
+ Revision: 685860
- make perl-doc sub-package noarch
- rebuild for perl(abi) deps
- fix duplicates in %%files list for perl-doc
- fix unpackaged directories

* Wed May 18 2011 Oden Eriksson <oeriksson@mandriva.com> 5.12.3-7
+ Revision: 675985
- P52: security fix for CVE-2011-1487

* Thu May 05 2011 Funda Wang <fwang@mandriva.org> 5.12.3-6
+ Revision: 669285
- clean up file list

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Thu Mar 31 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.12.3-5
+ Revision: 649377
- rebuild against db 5.1

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 5.12.3-4
+ Revision: 640284
- rebuild to obsolete old packages

* Thu Feb 10 2011 Funda Wang <fwang@mandriva.org> 5.12.3-3
+ Revision: 637156
- provides more perlapi

* Thu Feb 10 2011 Funda Wang <fwang@mandriva.org> 5.12.3-2
+ Revision: 637109
- add 5.12.2 as inc path

* Wed Feb 09 2011 Guillaume Rousse <guillomovitch@mandriva.org> 5.12.3-1
+ Revision: 637050
- update to new version 5.12.3

* Wed Jan 26 2011 Guillaume Rousse <guillomovitch@mandriva.org> 5.12.2-7
+ Revision: 633077
- set vendorman3dir explicitely too, otherwise it defaults to man3dir

* Wed Jan 26 2011 Guillaume Rousse <guillomovitch@mandriva.org> 5.12.2-6
+ Revision: 632993
- install man pages from core modules in section 3pm, to avoid conflict with standalone versions of the same modules

* Fri Nov 19 2010 Oden Eriksson <oeriksson@mandriva.com> 5.12.2-5mdv2011.0
+ Revision: 599067
- P51: fix borkiness with Compress::Zlib
- rediffed fuzzy patches

  + JÃ©rÃ´me Quelin <jquelin@mandriva.org>
    - remove path setting, which did not help

* Thu Sep 09 2010 GÃ¶tz Waschk <waschk@mandriva.org> 5.12.2-4mdv2011.0
+ Revision: 577004
- reenable checks

* Thu Sep 09 2010 GÃ¶tz Waschk <waschk@mandriva.org> 5.12.2-3mdv2011.0
+ Revision: 577002
- disable checks for bootstrapping

  + JÃ©rÃ´me Quelin <jquelin@mandriva.org>
    - not sure tests pick up the correct path
    - mdv#60956 - fix h2ph

* Thu Sep 09 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.12.2-2mdv2011.0
+ Revision: 576910
- fix #60939 - provides perl-libnet again

* Tue Sep 07 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.12.2-1mdv2011.0
+ Revision: 576627
- update to 5.12.2

* Fri Aug 06 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.12.1-3mdv2011.0
+ Revision: 566958
- perl-suid should be obsoleted, not conflicted

* Tue Jul 27 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.12.1-2mdv2011.0
+ Revision: 561874
- submitting directly to main/release

* Tue Jul 27 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.12.1-1mdv2011.0
+ Revision: 561860
- update perlapi and @INC list
- update to perl 5.12.1
- 5.12 is now current

* Fri Jun 11 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.10.1-10mdv2010.1
+ Revision: 547928
- 5.12 dvpt should be done in a branch
- forgot to commit tarball
- 5.12.0 final

* Wed Apr 07 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.12.0-0.RC4.1mdv2010.1
+ Revision: 532699
- update to 5.12.0-rc4

* Wed Mar 31 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.12.0-0.RC1.1mdv2010.1
+ Revision: 530267
- update to 5.12.0-rc1

* Fri Mar 26 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.12.0-0.RC0.1mdv2010.1
+ Revision: 527724
- rebuild
- *** /!\ WARNING /!\
- SUID emulation has been removed in perl 5.12
    Configure is now run without -Dd_dosuid
    ==> perl-suid package doesn't exist anymore
    perl-base now has a "Conflicts: perl-suid" to ensure smooth upgrade
  *** Patches changes
- patch 3: perl-5.10.1-RC1-norootcheck.patch
    merged upstream
    patch dropped
- patch 6: perl-5.8.8-RC1-fix-LD_RUN_PATH-for-MakeMaker.patch
    module moved to cpan/ExtUtils-MakeMaker
    patch rediffed
    renamed to perl-5.12.0-RC0-fix-LD_RUN_PATH-for-MakeMaker.patch
- patch 14: perl-5.12.0-RC0-install-files-using-chmod-644.patch
    module moved to dist/ExtUtils-Install
    renamed to perl-5.10.1-RC1-install-files-using-chmod-644.patch
- patch 16: perl-5.8.5-RC1-perldoc-use-nroff-compatibility-option.patch
    module moved to dist/Pod-Perldoc
    renamed to perl-5.12.0-RC0-perldoc-use-nroff-compatibility-option.patch
- patch 23: perl-5.10.1-patchlevel.patch
    update to match RC0
    renamed to perl-5.12.0-RC0-patchlevel.patch
- patch 24: perl-5.8.4-no-test-fcgi.patch
    test for FastCGI, which the CPAN version has a dependency on, but is not in core
    from #p5p:
    17:08:16 @Nicholas> yes, and I forget why, but I think that it
	became easier not to include it, as it would only skip in core.
    17:24:35 @Bram> It would not always skip in core. I believe that was
	the problem... (If the system perl has CGI::Fast installed and if it is
	the same version as the 'new' perl and the same INC path then the test
	woul pick up the CGI::Fast from the system and attempt to run the test
	(during make test that is))
    ==> patch dropped
- patch 29: perl-5.8.8-rpmdebug.patch
    module moved to cpan/ExtUtils-Manifest
    renamed to perl-5.12.0-RC0-rpmdebug.patch
- patch 42: perl-5.9.5-allow-to-override-core-modules.patch
- patch 43: perl-5.10.1-RC1-skip-tests-using-dev-log-for-iurt.patch
    module moved to cpan/Sys-Syslog
    renamed to perl-5.12.0-RC0-skip-tests-using-dev-log-for-iurt.patch

* Thu Dec 17 2009 Thierry Vignaud <tv@mandriva.org> 5.10.1-8mdv2010.1
+ Revision: 479695
- move File::Glob & Config_heavy.pl from perl into perl-base so that urpmi can
  work with only perl-base now that perl(Data::Dumper) is provided by both perl
  & perl-Data::Dumper
  hint: next time you package a more up-to-date perl module, remove it from
  perl and you check nothing got broken as a side effect

* Fri Dec 11 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.10.1-7mdv2010.1
+ Revision: 476552
- rebuild

* Mon Dec 07 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.10.1-6mdv2010.1
+ Revision: 474342
- bump mkrel
- dual-lifing pod::perldoc

* Mon Dec 07 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.10.1-5mdv2010.1
+ Revision: 474312
- bump mkrel
- given that dual-lived modules are in contrib, we should not use hard requires: deps but suggests:

* Sun Dec 06 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.10.1-4mdv2010.1
+ Revision: 474100
- bump mkrel
- requiring modules in order to have a perl as shipped upstream
  we removed them from base "perl" package in order to easily dual-life
  them, but there was a long thread on perl5 porters about the definition
  of package perl (on fedora).
  cf http://www.nntp.perl.org/group/perl.perl5.porters/2009/08/msg149747.html
- adding missing lowercase provides (if)
- obsoletes only strictly older modules

* Sun Sep 27 2009 Olivier Blin <blino@mandriva.org> 5.10.1-3mdv2010.0
+ Revision: 450264
- add missing sgidef.h header on mips (from Arnaud Patard)

* Mon Aug 24 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.10.1-2mdv2010.0
+ Revision: 420261
- force resubmit
- update to 5.10.1

* Sat Aug 08 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.10.1-0.rc1.2mdv2010.0
+ Revision: 411690
- no api/abi compatibility before 5.10.0 (thanks anssi)
- catching arch-dependant directories for old perls
- using parallel tests to build package faster

* Fri Aug 07 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.10.1-0.rc1.1mdv2010.0
+ Revision: 411238
- anssi is not sure regarding perlapi-5.10.1, so let's keep it by now
- no need to provides perlapi-5.10.1 according to anssi
- update to 5.10.1-RC1
- removed lots of patches merged upstream
- rediffed some patches to apply them cleanly
- fix a bit spec file
  (i'm not really sure with the provides of perlapi)

* Sun Jul 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 5.10.0-27mdv2010.0
+ Revision: 400306
- add an explicit devel(libperl) dependency on devel package, as required by any other package linked against libperl.so

* Fri Jul 17 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 5.10.0-26mdv2010.0
+ Revision: 396825
- rebuild to have new automatic provides extraction
- fixed license field

* Thu Apr 16 2009 Thierry Vignaud <tv@mandriva.org> 5.10.0-25mdv2009.1
+ Revision: 367772
- merge some fixes from debian:
- patch 53: Incorrect substitution optimization introduced in 5.10.0
  (debian #501178, perl #52658) (crash fix):
- patch 54: Fix memory corruption with in-place sorting (debian
  #498769, perl #54758) (segfault fix)
- patch 55: Fix a segmentation fault occurring in the mod_perl2 test
  suite (debian #475498, perl #33807)
- patch 56: Fix memory leak with qr// (debian #503975)
- patch 57: NULL checks
- patch 58: Fix a memory leak with Scalar::Util::weaken() (debian
  #506324)
- patch 59: Fix memory leak in // caused by single-char character
  class optimization (debian #503975, perl #59516)
- patch 60: Fix a reference counting bug in PerlIO::via that leads to
  memory corruption (debian #479698)
- patch 61: Fix crash on binary-or lvalue operation on qr//
  [rt.perl.org #54956]
- patch 62: Fix a segmentation fault with 'debugperl -Dm' (Upstream
  change 33388)
- patch 63: Prevent setpgrp from corrupting the stack (debian #512796)
- patch 70: [SECURITY] CVE-2005-0448 revisited: File::Path::rmtree no
  longer allows creating of setuid files (debian #286905)

* Sun Mar 22 2009 Anssi Hannula <anssi@mandriva.org> 5.10.0-24mdv2009.1
+ Revision: 360448
- fix more format string errors (format-string.patch)
- fix a format string error in public handy.h (format-string.patch)

* Mon Dec 15 2008 Oden Eriksson <oeriksson@mandriva.com> 5.10.0-23mdv2009.1
+ Revision: 314501
- rediff fuzzy patches
- rebuilt against db4.7

  + Pixel <pixel@mandriva.com>
    - fix segfault (#44228)

* Thu Sep 18 2008 Guillaume Rousse <guillomovitch@mandriva.org> 5.10.0-21mdv2009.0
+ Revision: 285750
- upstream patch: fix parameters passing slowdown

  + Pixel <pixel@mandriva.com>
    - provides perl(version) (#43238)

* Thu Sep 11 2008 Michael Scherer <misc@mandriva.org> 5.10.0-20mdv2009.0
+ Revision: 283680
- add security fix for #42628, and various whitespace automated fix

* Tue Aug 26 2008 Olivier Blin <blino@mandriva.org> 5.10.0-19mdv2009.0
+ Revision: 276193
- fix build of debug packages (new strip_and_check_elf_files does not handle DONT_STRIP if not exported)

* Tue Aug 19 2008 Pixel <pixel@mandriva.com> 5.10.0-18mdv2009.0
+ Revision: 273938
- bytes.pm uses bytes_heavy.pl, not bytes_heavy.pm
- move bytes_heavy.pm to perl-base (it is used by bytes.pm)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

* Wed Jun 11 2008 Thierry Vignaud <tv@mandriva.org> 5.10.0-15mdv2009.0
+ Revision: 218044
- rebuild

* Tue May 20 2008 Oden Eriksson <oeriksson@mandriva.com> 5.10.0-14mdv2009.0
+ Revision: 209505
- get rid of the db1-devel and db2-devel build deps, db4-devel is enough

* Tue Apr 01 2008 Pixel <pixel@mandriva.com> 5.10.0-13mdv2008.1
+ Revision: 191443
- try again to workaround a segfault (which is now a "clean" panic) (#34505)
- tentative to workaround a segfault (#34505)

* Thu Mar 27 2008 Olivier Blin <blino@mandriva.org> 5.10.0-11mdv2008.1
+ Revision: 190713
- really generate debug package (by not stripping files when running spec-helper hack)

* Fri Mar 14 2008 Pixel <pixel@mandriva.com> 5.10.0-10mdv2008.1
+ Revision: 187849
- move the perlapi-5.8.8 explicit conflict from perl to perl-base
  (since it is perl-base which provides perlapi-xxx)

* Thu Mar 13 2008 Olivier Blin <blino@mandriva.org> 5.10.0-9mdv2008.1
+ Revision: 187564
- fix segfault with array ties (patch submitted and merged upstream, RT #51636)

* Wed Mar 12 2008 Olivier Blin <blino@mandriva.org> 5.10.0-8mdv2008.1
+ Revision: 187133
- build with -g even when debugging is disabled (without enabling perl debugging)

  + Pixel <pixel@mandriva.com>
    - urpmi's priority upgrade must include perl-XML-Parser otherwise urpmi will fail to load Hal::Cdrom

* Mon Mar 10 2008 Pixel <pixel@mandriva.com> 5.10.0-7mdv2008.1
+ Revision: 183653
- urpmi's priority upgrade must include perl-Net-DBus otherwise urpmi will fail to load Hal::Cdrom

* Mon Mar 03 2008 Pixel <pixel@mandriva.com> 5.10.0-6mdv2008.1
+ Revision: 177964
- add Obsoletes/Provides on perl-File-Fetch perl-CPAN perl-IO-Zlib
  perl-Pod-Simple (which are included in main perl) (#37445)

* Tue Jan 22 2008 Pixel <pixel@mandriva.com> 5.10.0-5mdv2008.1
+ Revision: 156194
- provide perl-version (needed since we obsolete it)

* Mon Jan 21 2008 Pixel <pixel@mandriva.com> 5.10.0-4mdv2008.1
+ Revision: 155899
- add obsoletes on perl-version <= 0.74 (since perl now bundles it)
- move feature.pm to perl-base (esp. for "state", cf perldelta(1))
- keep module perl-Time-Piece outside of perl
- fix putting pod files in perl-doc
- keep modules perl-IO-Compress-Base outside of perl
- keep modules perl-IO-Compress-Zlib and perl-Archive-Extract outside of perl
- another fix for #36535, thanks to Mashrab Kuvatov
- fix using open :locale under UTF-8@cyrillic locale (mdvbz#36535)

* Tue Jan 15 2008 Pixel <pixel@mandriva.com> 5.10.0-3mdv2008.1
+ Revision: 152152
- move perlapi-5.10.0 provide to perl-base
- move Tie::Hash to perl-base (since module POSIX uses it)
- keep modules perl-Compress-Raw-Zlib and perl-Compress-Zlib outside of perl
- really fix asm/unistd.ph

* Mon Jan 14 2008 Pixel <pixel@mandriva.com> 5.10.0-2mdv2008.1
+ Revision: 151585
- fix asm/unistd.ph (through a fix in h2ph which could not handle glibc 2.7 asm/unistd.h)
- normalize call to h2ph
- also conflict with drakxtools-backend built with 5.8.8

* Mon Jan 14 2008 Pixel <pixel@mandriva.com> 5.10.0-1mdv2008.1
+ Revision: 151160
- also conflict perl-Digest-SHA1 built with 5.8.8 (perl-RPM4 requires perl-Digest-SHA1)
- disable test using /dev/log which is not available in iurt
- we do not want the perlapi-xxx require on installed perl
- adapt to "Source2" not being compressed anymore
- fix build

* Fri Dec 21 2007 Thierry Vignaud <tv@mandriva.org> 5.8.8-14mdv2008.1
+ Revision: 136449
- source 3: temporary prevent uploading perl since we would have to rebuild every binary package (postponed until early january)
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - switch to threading again
      (since it can be useful, and other distros have it enabled)
    - 5.10.0:
      o provide perlapi-5.10.0 so that binary modules can require it and ensure
	correct upgrades in the future (a la debian)
      o conflict with important perl packages that would break
	(we can't list them all)
      o not including bundled modules already in existing packages and would conflict:
	Archive::Tar, Digest::SHA, CPANPLUS, Module::CoreList, Module::Build
      o rediff patches: patch14, patch15 (lib64), patch32 (inversionlist), patch42
	(allow override core modules)
      o drop applied upstream patches: patch33, patch35 (Net::NNTP::body and
	Net::NNTP::head would need the fix too?), patch36, patch37, patch39,
	patch40, patch41, patch43
      o perlcc is no more

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Thu Nov 15 2007 Pixel <pixel@mandriva.com> 5.8.8-13mdv2008.1
+ Revision: 108943
- allow modules in site_perl and vendor_perl to override perl builtin modules (#33090)
- backport fix from Math-Complex-1.37 (#35488)
- handle Pod::Perldoc manpages in perl-doc through file list
- don't list twice Pod/Perldoc/* modules
- remove old broken perldiag special case
- fix security issue in regexp engine (#35333)
- adapt to man pages being compressed with lzma
- spec-helper script is no more, use the rpm macro instead
- fix weird *old* rgs typo (how did rpm build with this?!)
- fix compiling with gcc 4.2.x

  + Thierry Vignaud <tv@mandriva.org>
    - fix man pages

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    -Ud_longdbl on all sparcs (%%sunsparc)
    - do parallell build

* Mon Apr 30 2007 Pixel <pixel@mandriva.com> 5.8.8-12mdv2008.0
+ Revision: 19552
- explicit file provide /usr/bin/perl

* Mon Apr 23 2007 Pixel <pixel@mandriva.com> 5.8.8-11mdv2008.0
+ Revision: 17453
- remove bad provides libperl.so from perl
  (libperl.so is still provided by perl-base)


* Fri Mar 16 2007 Pixel <pixel@mandriva.com> 5.8.8-10mdv2007.1
+ Revision: 145069
- move some more files (needed to run XFdrake)

* Mon Feb 12 2007 Pixel <pixel@mandriva.com> 5.8.8-9mdv2007.1
+ Revision: 118871
- fix segfault (bugzilla #28537, perl #41442)

  + Rafael Garcia-Suarez <rgarciasuarez@mandriva.com>
    - ppc64 fixes from Gwenole Beauchesne (from CS3).
      Bunzip patches.
    - Import perl

* Sat Sep 09 2006 Thierry Vignaud <tvignaud@mandriva.com> 5.8.8-7mdv2007.0
- patch 38: do not defer sig11 (aka segfaulting, #18087)

* Mon May 15 2006 Oden Eriksson <oeriksson@mandriva.com> 5.8.8-6mdk
- rebuilt due to missing perl-doc package for x86_64

* Sat May 13 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.8-5mdk
- Rebuild with new rpm-mandriva-setup

* Thu May 04 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.8-4mdk
- Drop patch 20 (loading of .pm.gz files, no longer used in gi, could
  be done in pure perl with @INC hooks)

* Sun Mar 12 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.8-3mdk
- Remove PERL_DISABLE_PMC from the CCFLAGS, as requested by Audrey Tang
- Remove german translations

* Fri Mar 03 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.8-2mdk
- Integrate upstream patches:
- patch 34 (#27210): buglet in c2ph
- patch 35 (#27211): buglet in Net::NNTP
- patch 36 (#27359): make -d:Foo=bar work again
- patch 37 (#27363): include predefined gcc macros in translated system headers

* Wed Feb 01 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.8-1mdk
- 5.8.8
- Remove patch 12 (MakeMaker hack for old rpm conventions)
- Rediff patch 23
- Remove patches 34 and 35, integrated upstream

* Thu Jan 26 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.8-0.RC1.4mdk
- Turn on -g optimisation so perl is built without -DDEBUGGING

* Tue Jan 24 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.8-0.RC1.3mdk
- Add patch 34 (upstream 26920) : restore compatibility with swig
- Add patch 35 (upstream 26940) : fix suidperl bug

* Tue Jan 24 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.8-0.RC1.2mdk
- Add patch 33 (upstream 26536) to fix bug 20129

* Fri Jan 20 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.8-0.RC1.1mdk
- New version
- Rediff patches 20, 23, 29
- Remove half of patch 6, integrated upstream
- Remove patches 22, 26, 27, 28, 30, 31, 33, 34, integrated upstream
- Remove patch 25, obsolete
- Obsoletes perl-Test-Builder-Tester

* Thu Jan 19 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.7-9mdk
- lib64 fix to buildrequires (Per Øyvind Karlsen)
- Patch 34: upstream 26812, h2ph improvement, fixes build on linux-sparc64

* Thu Dec 01 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.7-8mdk
- Patch 33: fix for CVE-2005-3962

* Mon Nov 28 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.7-7mdk
- Upgrade core modules List::Util and Getopt::Long to latest CPAN versions
  (patches 30 and 31)
- Always set up @INC correctly even if older directories don't exist on the
  build machine (patch 32)

* Fri Nov 18 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.7-6mdk
- Patch 29: patch default MANIFEST.SKIP allow Module::Signature to work even
  when building rpms with debug packages enabled

* Fri Oct 21 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.7-5mdk
- BuildRequires recent rpm-mandriva-setup-build

* Tue Oct 18 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.7-4mdk
- Upgrade to Storable 2.15 (patch 28)
- Fix installation of sperl as setuid

* Wed Aug 10 2005 Pixel <pixel@mandriva.com> 5.8.7-3mdk
- on x86_64, bits/syscall.ph requires bits/wordsize.ph

* Tue Aug 02 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.7-2mdk
- Add patch 27 (CAN-2005-0448)

* Wed Jun 01 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.7-1mdk
- 5.8.7
- Define sitebin to /usr/local/bin and siteman* to /usr/local/man/...
- Replace Mandrakelinux by Mandriva Linux

* Thu May 19 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.7-0.RC1.1mdk
- 5.8.7 RC1
- Remove patch 27, 28, 29, 30, merged upstream

* Sat Apr 23 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.8.6-7mdk
- Put sperl and suidperl in their own package perl-suid

* Mon Feb 14 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.6-6mdk
- Add patches 28 et 30 (security updates)

* Mon Jan 31 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.6-5mdk
- Fix local root exploit and buffer overflow (patch 28) (perlbug #33990)

* Wed Jan 26 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.6-4mdk
- Move the Pod::Perldoc::* modules to perl-doc
- Add Artistic licence in doc

* Fri Jan 07 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.6-3mdk
- Fixes (or workarounds) for build issues on x86_64
- add a "debugging" flag to build perls with -D enabled

* Wed Dec 01 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.6-2mdk
- Integrate patch 23565 from the maint branch (as patch 27):
  MakeMaker's default MANIFEST.SKIP was borked

* Mon Nov 29 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.6-1mdk
- 5.8.6
- use "make test_harness_notty" for testing
- fix invocation of h2ph with correct libperl.so

* Fri Nov 12 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.6-0.RC1.1mdk
- New version 5.8.6-RC1
- Remove support for threads
- Remove bincompat directories (since we break binary compatibility)
- Remove patch 27, merged upstream

* Tue Nov 09 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.5-4mdk
- Upgrade to MIME::Base64 3.05 (for perl-MIME-tools, security update)
- BuildRequire: libgdbm_compat (bugs #12036 and #12136)

* Fri Aug 06 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.5-3mdk
- Fix for generation of unistd.ph on ppc (Christiaan Welvaart)

* Thu Jul 29 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.5-2mdk
- Add a patch to prevent including an empty rpath in .so files produced
  by MakeMaker

* Wed Jul 21 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.5-1mdk
- 5.8.5.
- Move unicore/PVA.pl into perl-base.

* Fri Jul 09 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.5-0.RC2.1mdk
- RC2. Remove patch #23063.

* Thu Jul 08 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.5-0.RC1.2mdk
- Merged patch #23063: perl wasn't able to upgrade a literal undef to
  UTF-8 anymore. This broke Gtk2.

* Thu Jul 08 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.5-0.RC1.1mdk
- New version
- Remove patches merged upstream
- Fix CPAN signature test when Module::Signature is installed

* Tue Jun 29 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-13mdk
- Move Getopt::Std from perl to perl-base
- Move some changelogs from perl to perl-doc

* Sat Jun 19 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-12mdk
- Move CORE/config.h from perl-devel to perl. This is necessary for MakeMaker
  (and thus CPAN.pm) to work.

* Wed Jun 16 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-11mdk
- Carp::Heavy should be in perl-base, as it's required by Carp.pm
- Add manually a provides for perl(Carp::Heavy)

* Mon Jun 14 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-10mdk
- Further h2ph patches.

* Sun Jun 13 2004 Robert Vojta <robert.vojta@mandrake.org> 5.8.4-9mdk
- patches 42 and 43 temporarily disabled (see #10035)

* Sat Jun 12 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-8mdk
- Remove redundant BuildRequires
- Add two more h2ph patches from the development branch

* Sat Jun 12 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-7mdk
- Add BuildRequires glibc-devel

* Fri Jun 11 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-6mdk
- integrate patch #22925 from the development branch :
  Make h2ph able to understand a limited set of inline functions.
  This fixes the generation of some .ph files.

* Wed Jun 09 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-5mdk
- Restore loading of .pm.gz files by adjusting patch #20

* Wed Jun 09 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-4mdk
- Add compilation flag -DPERL_DISABLE_PMC
- Rebuild with new gcc

* Thu May 27 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-3mdk
- Add a bunch of patches from the maintainance branch

* Thu May 06 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-2mdk
- psed(1) wasn't installed
- the manpage for perlivp(1) (which isn't installed) was installed
- remove perldiag.pod from perl-doc

* Fri Apr 23 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-1mdk
- 5.8.4
- remove setuidperl, it was a transient RC2 tryout
- the only setuid executable is sperl5.8.4
- force gcc optimisation level to -O1 on ppc
- disable test lib/CGI/t/fast.t, which may fail if perl-FCGI is already
  installed on the system.

* Sat Apr 17 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-0.RC2.1mdk
- RC2
- remove setuid bit on sperl and suidperl
- new setuid executable setuidperl
- use 'make test_harness' instead of 'make test'
- add a note in the 'perl -V' output to mention MandrakeSoft patches

* Wed Apr 07 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-0.RC1.2mdk
- Restore 5.8.1/i386-linux in the inc_version_list, at least until
  all the packages from the CPAN are upgraded

* Wed Apr 07 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.8.4-0.RC1.1mdk
- changed perl URL
- FHS-compliance patch is no longer needed
- A more recent Getopt::Long is now bundled with perl, remove it
- remove 5.8.1/i386-linux from the inc_version_list, because 5.8.1 is
  binary incompatible with every other 5.8.x
- Add Errno.pm to perl-base

