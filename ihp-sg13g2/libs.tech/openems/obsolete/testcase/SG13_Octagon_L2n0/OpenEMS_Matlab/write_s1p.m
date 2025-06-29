function write_s1p( type, freq, data, filename, ref, comment )
% write_s1p( type, freq, data, filename [,ref [,comment]] ) - write touchstone-file
% for ADS
% type      'z' for Z-Parameter touchstone-file
%           'y' for Y-Parameter touchstone-file
%           's' for S-Parameter touchstone-file
% freq      vector of frequencies (in Hz)
% data      (numports x numports x numfreq) matrix
% filename  filename of the file to create
% ref       (optional) reference impedance
% comment   (optional) written in the header
%
% (C) Sebastian Held <sebastian.held@gmx.de>
% Version 21. Feb 2006
%
% MODIFIED FOR 1_PORT DATA with data size 1 x frequencies
% by Volker Muehlhaus

if lower(type) == 'z'
    par_type = 'Z';
    if nargin < 5; ref = 1; end
elseif lower(type) == 'y'
    par_type = 'Y';
    if nargin < 5; ref = 1; end
elseif lower(type) == 's'
    par_type = 'S';
    if nargin < 5; ref = 50; end
else
    error( 'only z-, y- and s-parameters supported by now' );
end

if nargin < 6
    comment = '';
end

num_freq = size( data, 2 );

[fid, message] = fopen( filename, 'wt' );
if fid == -1
    error( message );
end

fprintf( fid, '%s\n', ['#   Hz   ' par_type '  RI   R   ' num2str(ref)] );
fprintf( fid, '%s\n', ['! ' comment] );

if size( data, 1 ) == 1
    write_data_s1p(data, fid, freq);
else
    error( 'FIXME - unhandled dimension' );
end

fclose( fid );
return;
end %write_touchstone()

function write_data_s1p(data, fid, freq)
% for 1-port devices
for f=1:length(freq)
    fprintf( fid, '%e  %e %e \n', freq(f), real(data(1,f)), imag(data(1,f)) ); %Frequenz
end
end %write_data_s1p()
