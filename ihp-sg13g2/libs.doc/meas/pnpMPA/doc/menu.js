//
// Define the behaviour of the tree, specify the structure of
// the web site and setup the menu entries
//
// Joust Outliner Version 2.4.1
// (c) Copyright 1996-1999, Alchemy Computing Limited. All rights reserved.
// This code may be freely copied and distributed provided that it is accompanied by this header.
//
// Do not modify anything between here and the "End of Joust" marker unless you know what you
// are doing.  You can find the latest version of Joust and all associated files and help at
// http://www.alchemy-computing.co.uk/joust/.  If you have any questions/problems or you want to be
// added to the Joust mailing list, send an eMail to joust@alchemy.demon.co.uk.
//
// Window Tilte
document.write("<title>pnpMPA (SG13)</title>");
function initialise() {
// Tell joust where to find the various index files it needs
index1 = "index.htm";
// Set up parameters to control menu behaviour
theMenu.autoScrolling = true;
theMenu.modalFolders = false;
theMenu.linkOnExpand = false;
theMenu.toggleOnLink = false;
theMenu.showAllAsLinks = false;
theMenu.savePage = true;
theMenu.tipText = "status";
theMenu.selectParents = false;
theMenu.name = "theMenu";
theMenu.container = "self.menu";
theMenu.reverseRef = "parent";
theMenu.contentFrame = "text";
theMenu.defaultTarget = "text";
// Initialise all the icons
initOutlineIcons(theMenu.imgStore);
// Now set up the menu with a whole lot of addEntry and addChild function calls
var level1ID = -1;
var level2ID = -1;
var level3ID = -1;
level1ID = theMenu.addEntry(-1, "Document", "Content", "content.htm", "");
level1ID = theMenu.addEntry(-1, "Folder", "Measurements Setup", "", "");
level2ID = theMenu.addChild(level1ID, "Folder", "Transistors", "", "");
level3ID = theMenu.addChild(level2ID, "Document", "pnpMPA", "setup/meas_pnpMPA.htm", "");
level2ID = theMenu.addChild(level1ID, "Folder", "Capacitances", "", "");
level3ID = theMenu.addChild(level2ID, "Document", "Capacitances", "setup/meas_cv.htm", "");
level1ID = theMenu.addEntry(-1, "Folder", "Devices Info", "", "");
level2ID = theMenu.addChild(level1ID, "Folder", "Transistors", "", "");
level3ID = theMenu.addChild(level2ID, "Document", "pnpMPA", "setup/dc.htm", "");
level2ID = theMenu.addChild(level1ID, "Folder", "Capacitances", "", "");
level2ID = theMenu.addChild(level2ID, "Document", "Capacitances", "setup/cv.htm", "");
level1ID = theMenu.addEntry(-1, "Folder", "Results", "", "");
level2ID = theMenu.addChild(level1ID, "Folder", "Transistor pnpMPA", "", "");
level3ID = theMenu.addChild(level2ID, "Document", "Gummel plots", "results/result_gummel_transistor_pnpMPA.htm", "");
level3ID = theMenu.addChild(level2ID, "Document", "Output characteristics", "results/result_output_transistor_pnpMPA.htm", "");
level2ID = theMenu.addChild(level1ID, "Folder", "Capacitances", "", "");
level3ID = theMenu.addChild(level2ID, "Document", "C_pnpMPA", "results/result_c_pnpMPA.htm", "");
level3ID = theMenu.addChild(level2ID, "Document", "PSD to Nwell", "results/result_c_PSD_nwell.htm", "");
level3ID = theMenu.addChild(level2ID, "Document", "Nwell to Substrate", "results/result_c_nwell_sub.htm", "");
level1ID = theMenu.addEntry(-1, "Folder", "Model Parameter Set", "", "");
level2ID = theMenu.addChild(level1ID, "Document", "pnpMPA", "results/library_transistor_pnpMPA.htm", "");
}
