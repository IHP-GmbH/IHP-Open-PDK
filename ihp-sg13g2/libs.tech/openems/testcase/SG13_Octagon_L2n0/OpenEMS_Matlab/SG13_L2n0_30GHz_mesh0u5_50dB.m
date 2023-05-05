%
% SG13 OpenEMS simulation - Volker testcase

close all
clear
clc
confirm_recursive_rmdir(0);   % delete old data without asking

basename = mfilename ; % get name of current model from *.m filename
physical_constants;    % load table of physical constants

%% setup the simulation %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

unit = 1e-6; % specify everything in um

Boundaries   = {'PEC' 'PEC' 'PEC' 'PEC' 'PEC' 'PEC'};  % xmin xmax ymin ymax zmin zmax

refined_cellsize = 0.5;  % mesh resolution in area with polygons from GDSII

f_start = 0e9;
f_stop  = 30e9;

energy_limit = -50;    % end criteria for residual energy

max_cellsize = c0/(f_stop*sqrt(11.9))/unit /20;  % max cellsize 1/20 wavelength in silicon


%% setup FDTD parameters & excitation function %%%%%%%%%%%%%%%%%%%%%%%%%%%%
lim = exp(energy_limit/10 * log(10)); % cconvert energy limit from dB to number
FDTD = InitFDTD('endCriteria',lim);
FDTD = SetGaussExcite(FDTD,0.5*(f_start+f_stop),0.5*(f_stop-f_start));
FDTD = SetBoundaryCond( FDTD, Boundaries );

CSX = InitCSX();

%%%%%%%%%%%%%%%%%%%%%%%%%  SG13G2 stackup  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% silicon substrate
CSX = AddMaterial( CSX, 'Sub' );
CSX = SetMaterialProperty( CSX, 'Sub', 'Epsilon', 11.9, 'Kappa', 2 );
Sub.thick = 280;
Sub.zmin = 0;
Sub.zmax = Sub.zmin + Sub.thick;

mesh.z = [linspace(Sub.zmin,Sub.zmax,20) ];


%% EPI
CSX = AddMaterial( CSX, 'EPI' );
CSX = SetMaterialProperty( CSX, 'EPI', 'Epsilon', 11.9, 'Kappa', 5 );
EPI.thick = 3.75;
EPI.zmin = Sub.zmax;
EPI.zmax = EPI.zmin + EPI.thick;

mesh.z = [mesh.z linspace(EPI.zmin,EPI.zmax,2)];


%% SiO2
CSX = AddMaterial( CSX, 'SiO2' );
CSX = SetMaterialProperty( CSX, 'SiO2', 'Epsilon', 4.1 );
SiO2.thick = 17.73;
SiO2.zmin = EPI.zmax;
SiO2.zmax = SiO2.zmin + SiO2.thick;

mesh.z = [mesh.z SiO2.zmin SiO2.zmax];


%% air above is background material, no need to place box, just add mesh line
Air.thick = 300;
Air.zmax = SiO2.zmax + Air.thick;
mesh.z = [mesh.z Air.zmax];


%% TopMetal2
TopMetal2.sigma = 30300000.0;
TopMetal2.thick = 3;
TopMetal2.zmin  = SiO2.zmin + 11.23;
TopMetal2.zmax  = TopMetal2.zmin + TopMetal2.thick;
CSX = AddMaterial( CSX, 'TopMetal2' );
CSX = SetMaterialProperty( CSX, 'TopMetal2', 'Kappa', TopMetal2.sigma );

mesh.z = [mesh.z linspace(TopMetal2.zmin,TopMetal2.zmax,3)];


%% TopMetal1
TopMetal1.sigma = 27800000.0;
TopMetal1.thick = 2;
TopMetal1.zmin  = SiO2.zmin + 6.43;
TopMetal1.zmax  = TopMetal1.zmin + TopMetal1.thick;
CSX = AddMaterial( CSX, 'TopMetal1' );
CSX = SetMaterialProperty( CSX, 'TopMetal1', 'Kappa', TopMetal1.sigma );

mesh.z = [mesh.z linspace(TopMetal1.zmin,TopMetal1.zmax,3)];

%% TopVia2
TopVia2.sigma = 3143000.0;
TopVia2.thick = 2.8;
TopVia2.zmin  = TopMetal1.zmax;
TopVia2.zmax  = TopVia2.zmin + TopVia2.thick;
CSX = AddMaterial( CSX, 'TopVia2' );
CSX = SetMaterialProperty( CSX, 'TopVia2', 'Kappa', TopVia2.sigma );



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  conductors  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Cell ("L_2n0_simplify", 10 polygons, 0 paths, 2 labels, 0 references)

clear p;
p(1,1) = 22.200;
p(2,1) = 0.000;
p(1,2) = 34.200;
p(2,2) = 0.000;
p(1,3) = 34.200;
p(2,3) = 57.000;
p(1,4) = 22.200;
p(2,4) = 57.000;
CSX = AddLinPoly( CSX, 'TopMetal1', 200, 'z', TopMetal1.zmin, p, TopMetal1.thick);
clear p;
p(1,1) = -34.200;
p(2,1) = 0.000;
p(1,2) = -22.200;
p(2,2) = 0.000;
p(1,3) = -22.200;
p(2,3) = 57.000;
p(1,4) = -34.200;
p(2,4) = 57.000;
CSX = AddLinPoly( CSX, 'TopMetal1', 200, 'z', TopMetal1.zmin, p, TopMetal1.thick);
clear p;
p(1,1) = -23.230;
p(2,1) = 272.000;
p(1,2) = -9.985;
p(2,2) = 272.000;
p(1,3) = 5.015;
p(2,3) = 257.000;
p(1,4) = 23.230;
p(2,4) = 257.000;
p(1,5) = 23.230;
p(2,5) = 269.000;
p(1,6) = 9.985;
p(2,6) = 269.000;
p(1,7) = -5.015;
p(2,7) = 284.000;
p(1,8) = -23.230;
p(2,8) = 284.000;
CSX = AddLinPoly( CSX, 'TopMetal1', 200, 'z', TopMetal1.zmin, p, TopMetal1.thick);
clear p;
p(1,1) = 11.230;
p(2,1) = 257.000;
p(1,2) = 41.425;
p(2,2) = 257.000;
p(1,3) = 100.000;
p(2,3) = 198.425;
p(1,4) = 100.000;
p(2,4) = 115.575;
p(1,5) = 41.425;
p(2,5) = 57.000;
p(1,6) = 22.200;
p(2,6) = 57.000;
p(1,7) = 22.200;
p(2,7) = 45.000;
p(1,8) = 46.395;
p(2,8) = 45.000;
p(1,9) = 112.000;
p(2,9) = 110.605;
p(1,10) = 112.000;
p(2,10) = 203.395;
p(1,11) = 46.395;
p(2,11) = 269.000;
p(1,12) = 11.230;
p(2,12) = 269.000;
CSX = AddLinPoly( CSX, 'TopMetal2', 200, 'z', TopMetal2.zmin, p, TopMetal2.thick);
clear p;
p(1,1) = -100.000;
p(2,1) = 115.575;
p(1,2) = -100.000;
p(2,2) = 198.425;
p(1,3) = -41.425;
p(2,3) = 257.000;
p(1,4) = -5.015;
p(2,4) = 257.000;
p(1,5) = 9.985;
p(2,5) = 272.000;
p(1,6) = 47.635;
p(2,6) = 272.000;
p(1,7) = 115.000;
p(2,7) = 204.635;
p(1,8) = 115.000;
p(2,8) = 109.365;
p(1,9) = 47.635;
p(2,9) = 42.000;
p(1,10) = -47.635;
p(2,10) = 42.000;
p(1,11) = -115.000;
p(2,11) = 109.365;
p(1,12) = -115.000;
p(2,12) = 204.635;
p(1,13) = -47.635;
p(2,13) = 272.000;
p(1,14) = -11.230;
p(2,14) = 272.000;
p(1,15) = -11.230;
p(2,15) = 284.000;
p(1,16) = -52.605;
p(2,16) = 284.000;
p(1,17) = -127.000;
p(2,17) = 209.605;
p(1,18) = -127.000;
p(2,18) = 104.395;
p(1,19) = -52.605;
p(2,19) = 30.000;
p(1,20) = 52.605;
p(2,20) = 30.000;
p(1,21) = 127.000;
p(2,21) = 104.395;
p(1,22) = 127.000;
p(2,22) = 209.605;
p(1,23) = 52.605;
p(2,23) = 284.000;
p(1,24) = 5.015;
p(2,24) = 284.000;
p(1,25) = -9.985;
p(2,25) = 269.000;
p(1,26) = -46.395;
p(2,26) = 269.000;
p(1,27) = -112.000;
p(2,27) = 203.395;
p(1,28) = -112.000;
p(2,28) = 110.605;
p(1,29) = -46.395;
p(2,29) = 45.000;
p(1,30) = -22.200;
p(2,30) = 45.000;
p(1,31) = -22.200;
p(2,31) = 57.000;
p(1,32) = -41.425;
p(2,32) = 57.000;
CSX = AddLinPoly( CSX, 'TopMetal2', 200, 'z', TopMetal2.zmin, p, TopMetal2.thick);
clear p;
p(1,1) = -22.610;
p(2,1) = 272.620;
p(1,2) = -11.860;
p(2,2) = 272.620;
p(1,3) = -11.860;
p(2,3) = 283.370;
p(1,4) = -22.610;
p(2,4) = 283.370;
CSX = AddLinPoly( CSX, 'TopVia2', 200, 'z', TopVia2.zmin, p, TopVia2.thick);
clear p;
p(1,1) = 11.850;
p(2,1) = 257.620;
p(1,2) = 22.600;
p(2,2) = 257.620;
p(1,3) = 22.600;
p(2,3) = 268.370;
p(1,4) = 11.850;
p(2,4) = 268.370;
CSX = AddLinPoly( CSX, 'TopVia2', 200, 'z', TopVia2.zmin, p, TopVia2.thick);
clear p;
p(1,1) = -33.580;
p(2,1) = 45.620;
p(1,2) = -22.830;
p(2,2) = 45.620;
p(1,3) = -22.830;
p(2,3) = 56.370;
p(1,4) = -33.580;
p(2,4) = 56.370;
CSX = AddLinPoly( CSX, 'TopVia2', 200, 'z', TopVia2.zmin, p, TopVia2.thick);
clear p;
p(1,1) = 22.820;
p(2,1) = 45.620;
p(1,2) = 33.570;
p(2,2) = 45.620;
p(1,3) = 33.570;
p(2,3) = 56.370;
p(1,4) = 22.820;
p(2,4) = 56.370;
CSX = AddLinPoly( CSX, 'TopVia2', 200, 'z', TopVia2.zmin, p, TopVia2.thick);

% Bounding box of geometry
geometry.xmin= -127.000;
geometry.xmax= 127.000;
geometry.ymin= 0.000;
geometry.ymax= 284.000;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%  end of conductors  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%  ports created manually  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[CSX, port] = AddLumpedPort( CSX, 500, 1, 50, [-22.2 0 TopMetal1.zmin], [22.2 10 TopMetal1.zmax], [1 0 0], true);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  end of ports  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

geometry.width = geometry.xmax - geometry.xmin;
geometry.height = geometry.ymax - geometry.ymin;

% for inductors, add margin of one inductor diameter on each side, so that metal walls have no effect
box.xmin = geometry.xmin - 1.0 * geometry.width;
box.xmax = geometry.xmax + 1.0 * geometry.width;
box.ymin = geometry.ymin - 1.0 * geometry.height;
box.ymax = geometry.ymax + 1.0 * geometry.height;


%%%%%%%%%%%%%%%%%%%%% boxes for dielectrics and substrate %%%%%%%%%%%%%%%%%%%%%%%%%%

CSX = AddBox( CSX, 'Sub', 0, [box.xmin, box.ymin, Sub.zmin], [box.xmax, box.ymax, Sub.zmax] );
CSX = AddBox( CSX, 'EPI', 0, [box.xmin, box.ymin, EPI.zmin], [box.xmax, box.ymax, EPI.zmax] );
CSX = AddBox( CSX, 'SiO2', 0, [box.xmin, box.ymin, SiO2.zmin], [box.xmax, box.ymax, SiO2.zmax] );


%%%%%%%%%%%%%%%%%%%%%%%%%%%  build final mesh   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

mesh.x = [box.xmin box.xmax];
mesh.y = [box.ymin box.ymax];

% refine mesh in conductor regions
mesh.x = [mesh.x linspace(geometry.xmin, geometry.xmax, geometry.width/refined_cellsize)];
mesh.y = [mesh.y linspace(geometry.ymin, geometry.ymax, geometry.height/refined_cellsize)];

mesh.x = SmoothMeshLines( mesh.x, max_cellsize, 1.3, 0);
mesh.y = SmoothMeshLines( mesh.y, max_cellsize, 1.3, 0);
mesh.z = SmoothMeshLines( mesh.z, max_cellsize, 1.3, 0);

CSX = DefineRectGrid( CSX, unit, mesh );


%% write/show/run the openEMS compatible xml-file
Sim_Path = ['data/' basename];
Sim_CSX = [basename '.xml'];

[status, message, messageid] = rmdir( Sim_Path, 's' ); % clear previous directory
[status, message, messageid] = mkdir( Sim_Path ); % create empty simulation folder

WriteOpenEMS( [Sim_Path '/' Sim_CSX], FDTD, CSX );

CSXGeomPlot( [Sim_Path '/' Sim_CSX] );  % open in viewer before start
RunOpenEMS( Sim_Path, Sim_CSX ,'');  % start solver

%% post-processing
close all
f = linspace( f_start, f_stop, 1601 );
port = calcPort(port, Sim_Path, f, 'RefImpedance', 50);

s11 = port.uf.ref./ port.uf.inc;
Zin = port.uf.tot ./ port.if.tot;

%% plot results

% S11
plot(f/1e9,20*log10(abs(s11)),'r-','LineWidth',2);
figure 1;
grid on;
ylabel('|S_11| (dB)','Interpreter','None');
xlabel('frequency (GHz)');

% Rseries
Rseries = real(Zin);
figure 2;
plot(f/1e9,Rseries,'r-','LineWidth',2);
ylim([0 10]);
grid on;
ylabel('Rseries');
xlabel('frequency (GHz)');

% Lseries
omega = 2*pi*f;
Lseries = imag(Zin)./omega;
figure 3;
plot(f/1e9,Lseries*1e9,'r-','LineWidth',2);
ylim([0 5]);
grid on;
ylabel('Lseries [nH]');
xlabel('frequency (GHz)');

% Q factor
Q = imag(Zin)./real(Zin);
figure 4;
plot(f/1e9,Q,'r-','LineWidth',2);
ylim([0 30]);
grid on;
ylabel('Q factor');
xlabel('frequency (GHz)');

save ([Sim_Path '/results']);

%% export Touchstone *.s1p
write_s1p('s',f,s11,[Sim_Path '/' basename '.s1p'],50);




