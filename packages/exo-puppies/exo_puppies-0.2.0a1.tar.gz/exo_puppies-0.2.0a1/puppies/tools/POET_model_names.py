# ASTRO
#"mandelecl"    ["midpt",  "width",  "depth",  "tin",  "teg",  "flux"]
"mandelecl2"   ["midpt2", "width2", "depth2", "tin2", "teg2", "flux2"]
"mandelecl3"   ["midpt3", "width3", "depth3", "tin3", "teg3", "flux3"]
#"mandeltr"     ["epoch", "rprs", "cosi", "ars", "flux", "per",
#                 "C1", "C2", "C3", "C4"]
"trnlldsp2"    ["trspmid2", "rprs2", "cosi2", "ars2", "trspf2", "trspp2",
                 "C12", "C22", "C32", "C42"]
"mandelgeom"   ["midpt", "width", "Rp/Rs", "b", "flux"]
"mandelorbit"  ["e", "omega", "i", "period", "rplanet", "rstar", "mstar",
                 "ecldepth", "flux"]

# RAMPS
#"expamp",     ["goal", "r0", "r1", "pm"]
#"linramp",    ["r1", "r0", "t0"]
#"quadramp",   ["qrr3", "qrr2", "qrc", "qrt0"]
"selramp",    ["selgoal", "selr0", "selr1", "selr2", "selt0", "selpm"]
"seqramp",    ["seqgoal", "seqr0", "seqr1", "seqr2", "seqr3", "seqt0", "seqpm"]
"se2ramp",    ["se2goal", "se2r0", "se2r1", "se2pm0", "se2r4", "se2r5", "se2pm1"]
"llramp",     ["llt0", "llr6", "llr2", "llc", "llt1"]
"lqramp",     ["lqt0", "lqr6", "lqr7", "lqr2", "lqc", "lqt1"]
"logramp",    ["logt0", "logr9", "logr8", "logr7", "logr6", "logc"]
"log4qramp",  ["l4qt0", "l4qr9", "l4qr8", "l4qr7", "l4qr6", "l4qr3", "l4qr2", "l4qc", "l4qt1"]
"relramp",    ["goal", "m", "t0", "a", "b", "t1"]
"reqramp",    ["goal", "m", "t0", "a", "b", "c", "t1"]
"re2ramp",    ["goal", "a", "m1", "t1", "b", "m2", "t2"]
"fallingexp", ["goal", "m", "t0"]
"felramp",    ["goal", "m", "t0", "a", "t1"]
"sindecay",   ["x0", "a", "b", "c", "d"]
"sincos",     ["a", "p1", "t1", "b", "p2", "t2", "c"]

#INTRAPIXEL / INTERPOLATION
#"bilinint",     []
"linip",        ["y0", "x0", "y1", "x1", "y2", "x2", "y3", "x3", "y4", "x4",
                 "y5", "x5", "y6", "x6", "y7", "x7", "y8", "x8"]
"quadip",       ["a", "b", "c", "d", "e", "f"]
"quadip4",      ["a", "b", "c", "d", "e", "f"]
"cubicip",      ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
"sexticip",     ["y6", "x6", "y5", "x5", "y4", "x4", "y3", "x3",
                 "y2", "x2", "y1", "x1", "c"]
"sexticipc",    ["y6", "x6", "y5", "x5", "y4", "x4", "y3", "x3", "y2x", "x2y",
                 "y2", "x2", "xy", "y1", "x1", "c"]
"posfluxlinip", ["p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8",
                 "y0", "x0", "y1", "x1", "y2", "x2", "y3", "x3", "y4", "x4",
                 "y5", "x5", "y6", "x6", "y7", "x7", "y8", "x8"]
"ballardip",    ["sigmay", "sigmax", "nbins"]
"medianip",     ["rad"]
"nnint",        ["minpts"]
"ipspline",     ["yknots", "xknots"]

#OTHERS
"aorflux",       ["a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"]
"posflux",       ["p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8"]
"posflux2",      ["p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8"]
"vsll",          ["vsx0", "vsa", "vsb", "vsc", "vsx1"]
"vsspline",      ["k0", "k1", "k2", "k3", "k4", "k5", "k6", "k7", "k8",
                  "k9", "k10", "k11"]
"flatfield3",    ["f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "flux"]
"expramp",       ["goal", "m", "a"]
"not0risingexp", ["goal", "m", "a", "b", "c"]
