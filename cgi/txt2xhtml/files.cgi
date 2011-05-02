#!/usr/bin/perl -w

# ���W���[���ǂݍ���
use strict;
use CGI;
use File::Temp;
use File::Find;
use Time::Piece;
use File::Copy;

our @filelist = ();


# �I�u�W�F�N�g�쐬
my $query = CGI->new;
# ���[�U���擾
my $user=$ENV{'REMOTE_USER'};

# �t�@�C���擾
my $output_directory = "/home/aozora-bunko/www/txt2xhtml/output/$user/";
my $input_directory = "/home/aozora-bunko/www/txt2xhtml/input/$user/";

# HTML�o��
print $query->header(-charset=>'Shift_JIS'),
      $query->start_html(-lang=>'ja', -encoding=>'Shift_JIS', -title=>'txt2xhtml');

print "<h2>�t�@�C�����X�g<\/h2>";
print "<p>�����ł́A��ƃt�@�C���̑|���Ɖ摜�t�@�C�����̃A�b�v���[�h���ł��܂�<\/p>";


print "<h3>�A�b�v���[�h<\/h3>";
my $upload_filename = $query->param('uploadfile');
if ($upload_filename)
{
print "Uploading file ... $upload_filename";
# �t�@�C���擾
my $fH = $query->upload('uploadfile');
my ($buffer);
# MIME�^�C�v�擾
my $mimetype = $query->uploadInfo($fH)->{'Content-Type'};
my $tmp_filename = "$output_directory/$upload_filename";
# �t�@�C���ۑ�
open (OUT, ">$tmp_filename") || die "Can't open input file!";
binmode (OUT);
while(read($fH, $buffer, 1024)){
    print OUT $buffer;
}
close (OUT);
close ($fH) if ($CGI::OS ne 'UNIX'); # Windows�v���b�g�t�H�[���p
chmod (0666, $tmp_filename);
}

print $query->start_form;
print $query->filefield('-name' => 'uploadfile');
print $query->submit('-name' => "�A�b�v���[�h"), $query->reset;
print $query->end_form;

print "<h3>�|��<\/h3>";
my @filename = $query->param('filename');
if (@filename)
{
print "Deleting ... @filename";
unlink @filename;
}
# find( sub {print "$File::Find::name$/" if (/\.html$/)},$output_directory);
find(\&wanted, $output_directory);


# my @filelist = ("a","b","c");
print "<p>��������t�@�C����I��ő|��<\/p>";
print $query->start_form;
print $query->checkbox_group('-name' => 'filename',-values => \@filelist,-columns=>1);
print $query->submit('-name' => "����"), $query->reset;
print $query->end_form;

print "<h3>�_�E�����[�h<\/h3>";
print $query->start_form(-action => "/cgi-bin/download2.cgi");
print $query->radio_group('-name' => 'file',-values => \@filelist,-columns=>1);
print $query->submit('-name' => "�_�E�����[�h"), $query->reset;
print $query->end_form;

print "<p><a href=\"\/\">�߂�<\/a><\/p>";
print $query->end_html;

#--------------------------------------------
#�t�@�C����������x�ɌĂяo�����
#--------------------------------------------
sub wanted{
#  print $File::Find::dir, '/';    #�J�����g�f�B���N�g��
#  print $_;          #�t�@�C����
#  print "\n";

  #�t���p�X�̃t�@�C����
push @filelist,$File::Find::name if /\.(png|html)$/si;
}
exit;
