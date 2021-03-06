#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import sympy as _sympy

#
#  Human-readable version is at:
#    [srcdir]/docs/abbreviations/abbr_ref_book.pdf
#
#  Atom number must be one of following presentations.
#  Available:
#    1) _sympy.Integer(x) => An integer [x].
#    2) _sympy.Rational(numerator, denominator) => A fraction [numerator / denominator].
#
ABBREVIATIONS = {
    "ACN": {"H": _sympy.Integer(3),
            "C": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "AcOH": {"H": _sympy.Integer(4),
             "C": _sympy.Integer(2),
             "O": _sympy.Integer(2)},
    "t-BuOH": {"H": _sympy.Integer(10),
               "C": _sympy.Integer(4),
               "O": _sympy.Integer(1)},
    "DCM": {"H": _sympy.Integer(2),
            "C": _sympy.Integer(1),
            "Cl": _sympy.Integer(2)},
    "DMA": {"H": _sympy.Integer(9),
            "C": _sympy.Integer(4),
            "O": _sympy.Integer(1),
            "N": _sympy.Integer(1)},
    "DMF": {"H": _sympy.Integer(7),
            "C": _sympy.Integer(3),
            "O": _sympy.Integer(1),
            "N": _sympy.Integer(1)},
    "DMPU": {"H": _sympy.Integer(12),
             "C": _sympy.Integer(6),
             "O": _sympy.Integer(1),
             "N": _sympy.Integer(2)},
    "DMSO": {"H": _sympy.Integer(6),
             "S": _sympy.Integer(1),
             "C": _sympy.Integer(2),
             "O": _sympy.Integer(1)},
    "EtOH": {"H": _sympy.Integer(6),
             "C": _sympy.Integer(2),
             "O": _sympy.Integer(1)},
    "HMPT": {"H": _sympy.Integer(18),
             "P": _sympy.Integer(1),
             "C": _sympy.Integer(6),
             "O": _sympy.Integer(1),
             "N": _sympy.Integer(3)},
    "MeOH": {"H": _sympy.Integer(4),
             "C": _sympy.Integer(1),
             "O": _sympy.Integer(1)},
    "TMBE": {"H": _sympy.Integer(12),
             "C": _sympy.Integer(5),
             "O": _sympy.Integer(1)},
    "MTBE": {"H": _sympy.Integer(12),
             "C": _sympy.Integer(5),
             "O": _sympy.Integer(1)},
    "PEG-r": {"H": _sympy.Integer(4),
              "C": _sympy.Integer(2),
              "O": _sympy.Integer(1)},
    "TFA": {"H": _sympy.Integer(1),
            "C": _sympy.Integer(2),
            "F": _sympy.Integer(3),
            "O": _sympy.Integer(2)},
    "THF": {"H": _sympy.Integer(8),
            "C": _sympy.Integer(4),
            "O": _sympy.Integer(1)},
    "9-BBN": {"H": _sympy.Integer(30),
              "B": _sympy.Integer(2),
              "C": _sympy.Integer(16)},
    "ACAC": {"H": _sympy.Integer(8),
             "C": _sympy.Integer(5),
             "O": _sympy.Integer(2)},
    "AIBN": {"H": _sympy.Integer(12),
             "C": _sympy.Integer(8),
             "N": _sympy.Integer(4)},
    "BTI": {"H": _sympy.Integer(5),
            "I": _sympy.Integer(1),
            "C": _sympy.Integer(10),
            "F": _sympy.Integer(6),
            "O": _sympy.Integer(4)},
    "BuLi": {"H": _sympy.Integer(9),
             "Li": _sympy.Integer(1),
             "C": _sympy.Integer(4)},
    "BOP": {"H": _sympy.Integer(22),
            "P": _sympy.Integer(2),
            "O": _sympy.Integer(1),
            "F": _sympy.Integer(6),
            "C": _sympy.Integer(12),
            "N": _sympy.Integer(6)},
    "CDI": {"H": _sympy.Integer(6),
            "C": _sympy.Integer(7),
            "O": _sympy.Integer(1),
            "N": _sympy.Integer(4)},
    "COD": {"H": _sympy.Integer(12),
            "C": _sympy.Integer(8)},
    "COT": {"H": _sympy.Integer(8),
            "C": _sympy.Integer(8)},
    "CPD": {"H": _sympy.Integer(6),
            "C": _sympy.Integer(5)},
    "CSA": {"H": _sympy.Integer(16),
            "S": _sympy.Integer(1),
            "C": _sympy.Integer(10),
            "O": _sympy.Integer(4)},
    "DABCO": {"H": _sympy.Integer(12),
              "C": _sympy.Integer(6),
              "N": _sympy.Integer(2)},
    "DADO": {"H": _sympy.Integer(8),
             "C": _sympy.Integer(4),
             "O": _sympy.Integer(2),
             "N": _sympy.Integer(2)},
    "DIBAH": {"H": _sympy.Integer(38),
              "C": _sympy.Integer(16),
              "Al": _sympy.Integer(2)},
    "DIBAL": {"H": _sympy.Integer(38),
              "C": _sympy.Integer(16),
              "Al": _sympy.Integer(3)},
    "DIBAL-H": {"H": _sympy.Integer(38),
                "C": _sympy.Integer(16),
                "Al": _sympy.Integer(4)},
    "DBU": {"H": _sympy.Integer(16),
            "C": _sympy.Integer(9),
            "N": _sympy.Integer(2)},
    "DBN": {"H": _sympy.Integer(12),
            "C": _sympy.Integer(7),
            "N": _sympy.Integer(2)},
    "DBPO": {"H": _sympy.Integer(10),
             "C": _sympy.Integer(14),
             "O": _sympy.Integer(4)},
    "BPO": {"H": _sympy.Integer(10),
            "C": _sympy.Integer(14),
            "O": _sympy.Integer(5)},
    "DCC": {"H": _sympy.Integer(22),
            "C": _sympy.Integer(13),
            "N": _sympy.Integer(2)},
    "DIC": {"H": _sympy.Integer(14),
            "C": _sympy.Integer(7),
            "N": _sympy.Integer(2)},
    "DEAD": {"H": _sympy.Integer(10),
             "C": _sympy.Integer(6),
             "O": _sympy.Integer(4),
             "N": _sympy.Integer(2)},
    "DIAD": {"H": _sympy.Integer(14),
             "C": _sympy.Integer(8),
             "O": _sympy.Integer(4),
             "N": _sympy.Integer(2)},
    "DMAP": {"H": _sympy.Integer(10),
             "C": _sympy.Integer(7),
             "N": _sympy.Integer(2)},
    "DNPH": {"H": _sympy.Integer(6),
             "C": _sympy.Integer(6),
             "O": _sympy.Integer(4),
             "N": _sympy.Integer(4)},
    "EDC": {"H": _sympy.Integer(17),
            "C": _sympy.Integer(8),
            "N": _sympy.Integer(3)},
    "HATU": {"H": _sympy.Integer(15),
             "P": _sympy.Integer(1),
             "O": _sympy.Integer(1),
             "F": _sympy.Integer(6),
             "C": _sympy.Integer(10),
             "N": _sympy.Integer(6)},
    "HexLi": {"H": _sympy.Integer(13),
              "Li": _sympy.Integer(1),
              "C": _sympy.Integer(6)},
    "HMDS": {"H": _sympy.Integer(19),
             "Si": _sympy.Integer(2),
             "C": _sympy.Integer(6),
             "N": _sympy.Integer(1)},
    "HOBt": {"H": _sympy.Integer(5),
             "C": _sympy.Integer(6),
             "O": _sympy.Integer(1),
             "N": _sympy.Integer(3)},
    "IDCP": {"H": _sympy.Integer(22),
             "I": _sympy.Integer(1),
             "O": _sympy.Integer(4),
             "Cl": _sympy.Integer(1),
             "C": _sympy.Integer(16),
             "N": _sympy.Integer(2)},
    "LAH": {"H": _sympy.Integer(4),
            "Li": _sympy.Integer(1),
            "Al": _sympy.Integer(1)},
    "LDA": {"H": _sympy.Integer(14),
            "Li": _sympy.Integer(1),
            "C": _sympy.Integer(6),
            "N": _sympy.Integer(1)},
    "mCPBA": {"H": _sympy.Integer(5),
              "C": _sympy.Integer(7),
              "Cl": _sympy.Integer(1),
              "O": _sympy.Integer(3)},
    "MeLi": {"H": _sympy.Integer(3),
             "Li": _sympy.Integer(1),
             "C": _sympy.Integer(1)},
    "MoOPD": {"H": _sympy.Integer(17),
              "Mo": _sympy.Integer(1),
              "C": _sympy.Integer(11),
              "N": _sympy.Integer(3),
              "O": _sympy.Integer(6)},
    "MoOPH": {"H": _sympy.Integer(23),
              "P": _sympy.Integer(1),
              "Mo": _sympy.Integer(1),
              "O": _sympy.Integer(6),
              "C": _sympy.Integer(11),
              "N": _sympy.Integer(3)},
    "NBS": {"H": _sympy.Integer(4),
            "Br": _sympy.Integer(1),
            "C": _sympy.Integer(4),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "NCS": {"H": _sympy.Integer(4),
            "O": _sympy.Integer(2),
            "C": _sympy.Integer(4),
            "Cl": _sympy.Integer(1),
            "N": _sympy.Integer(1)},
    "NHS": {"H": _sympy.Integer(5),
            "C": _sympy.Integer(4),
            "O": _sympy.Integer(3),
            "N": _sympy.Integer(1)},
    "PCC": {"H": _sympy.Integer(6),
            "N": _sympy.Integer(1),
            "Cl": _sympy.Integer(1),
            "Cr": _sympy.Integer(1),
            "C": _sympy.Integer(5),
            "O": _sympy.Integer(3)},
    "PIFA": {"H": _sympy.Integer(5),
             "I": _sympy.Integer(1),
             "C": _sympy.Integer(10),
             "F": _sympy.Integer(6),
             "O": _sympy.Integer(4)},
    "PyBOP": {"H": _sympy.Integer(28),
              "P": _sympy.Integer(2),
              "O": _sympy.Integer(1),
              "F": _sympy.Integer(6),
              "C": _sympy.Integer(18),
              "N": _sympy.Integer(6)},
    "sec-BuLi": {"H": _sympy.Integer(9),
                 "Li": _sympy.Integer(1),
                 "C": _sympy.Integer(4)},
    "TADDOL": {"H": _sympy.Integer(30),
               "C": _sympy.Integer(31),
               "O": _sympy.Integer(4)},
    "TBTU": {"H": _sympy.Integer(16),
             "O": _sympy.Integer(1),
             "F": _sympy.Integer(4),
             "B": _sympy.Integer(1),
             "C": _sympy.Integer(11),
             "N": _sympy.Integer(5)},
    "TEMPO": {"H": _sympy.Integer(18),
              "C": _sympy.Integer(9),
              "O": _sympy.Integer(1),
              "N": _sympy.Integer(1)},
    "tert-BuLi": {"H": _sympy.Integer(9),
                  "Li": _sympy.Integer(1),
                  "C": _sympy.Integer(4)},
    "t-BuLi": {"H": _sympy.Integer(10),
               "Li": _sympy.Integer(1),
               "C": _sympy.Integer(4)},
    "TESOTf": {"H": _sympy.Integer(15),
               "Si": _sympy.Integer(1),
               "C": _sympy.Integer(8),
               "F": _sympy.Integer(3),
               "O": _sympy.Integer(2)},
    "TMEDA": {"H": _sympy.Integer(16),
              "C": _sympy.Integer(6),
              "N": _sympy.Integer(2)},
    "TosMIC": {"H": _sympy.Integer(9),
               "S": _sympy.Integer(1),
               "C": _sympy.Integer(9),
               "O": _sympy.Integer(2),
               "N": _sympy.Integer(1)},
    "Ala": {"H": _sympy.Integer(7),
            "C": _sympy.Integer(3),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "Arg": {"H": _sympy.Integer(14),
            "C": _sympy.Integer(6),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(4)},
    "Asn": {"H": _sympy.Integer(8),
            "C": _sympy.Integer(4),
            "O": _sympy.Integer(3),
            "N": _sympy.Integer(2)},
    "Asp": {"H": _sympy.Integer(7),
            "C": _sympy.Integer(4),
            "O": _sympy.Integer(4),
            "N": _sympy.Integer(1)},
    "Cys": {"H": _sympy.Integer(7),
            "S": _sympy.Integer(1),
            "C": _sympy.Integer(3),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "Gln": {"H": _sympy.Integer(10),
            "C": _sympy.Integer(5),
            "O": _sympy.Integer(3),
            "N": _sympy.Integer(2)},
    "Glu": {"H": _sympy.Integer(9),
            "C": _sympy.Integer(5),
            "O": _sympy.Integer(4),
            "N": _sympy.Integer(1)},
    "Gly": {"H": _sympy.Integer(5),
            "C": _sympy.Integer(2),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "His": {"H": _sympy.Integer(9),
            "C": _sympy.Integer(6),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(3)},
    "Ile": {"H": _sympy.Integer(13),
            "C": _sympy.Integer(6),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "Leu": {"H": _sympy.Integer(13),
            "C": _sympy.Integer(6),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "Lys": {"H": _sympy.Integer(14),
            "C": _sympy.Integer(6),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(2)},
    "Met": {"H": _sympy.Integer(11),
            "S": _sympy.Integer(1),
            "C": _sympy.Integer(5),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "Phe": {"H": _sympy.Integer(11),
            "C": _sympy.Integer(9),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "Pro": {"H": _sympy.Integer(9),
            "C": _sympy.Integer(5),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "Pyl": {"H": _sympy.Integer(21),
            "C": _sympy.Integer(12),
            "O": _sympy.Integer(3),
            "N": _sympy.Integer(3)},
    "Sec": {"H": _sympy.Integer(7),
            "Se": _sympy.Integer(1),
            "C": _sympy.Integer(3),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "Ser": {"H": _sympy.Integer(7),
            "C": _sympy.Integer(3),
            "O": _sympy.Integer(3),
            "N": _sympy.Integer(1)},
    "Thr": {"H": _sympy.Integer(9),
            "C": _sympy.Integer(4),
            "O": _sympy.Integer(3),
            "N": _sympy.Integer(1)},
    "Trp": {"H": _sympy.Integer(12),
            "C": _sympy.Integer(11),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(2)},
    "Tyr": {"H": _sympy.Integer(11),
            "C": _sympy.Integer(9),
            "O": _sympy.Integer(3),
            "N": _sympy.Integer(1)},
    "Val": {"H": _sympy.Integer(11),
            "C": _sympy.Integer(5),
            "O": _sympy.Integer(2),
            "N": _sympy.Integer(1)},
    "A": {"H": _sympy.Integer(13),
          "C": _sympy.Integer(10),
          "O": _sympy.Integer(4),
          "N": _sympy.Integer(5)},
    "dA": {"H": _sympy.Integer(13),
           "C": _sympy.Integer(10),
           "O": _sympy.Integer(3),
           "N": _sympy.Integer(5)},
    "G": {"H": _sympy.Integer(13),
          "C": _sympy.Integer(10),
          "O": _sympy.Integer(5),
          "N": _sympy.Integer(5)},
    "dG": {"H": _sympy.Integer(13),
           "C": _sympy.Integer(10),
           "O": _sympy.Integer(4),
           "N": _sympy.Integer(5)},
    "C": {"H": _sympy.Integer(13),
          "C": _sympy.Integer(9),
          "O": _sympy.Integer(5),
          "N": _sympy.Integer(3)},
    "dC": {"H": _sympy.Integer(13),
           "C": _sympy.Integer(9),
           "O": _sympy.Integer(4),
           "N": _sympy.Integer(3)},
    "T": {"H": _sympy.Integer(14),
          "C": _sympy.Integer(10),
          "O": _sympy.Integer(6),
          "N": _sympy.Integer(2)},
    "dT": {"H": _sympy.Integer(14),
           "C": _sympy.Integer(10),
           "O": _sympy.Integer(5),
           "N": _sympy.Integer(2)},
    "U": {"H": _sympy.Integer(12),
          "C": _sympy.Integer(9),
          "O": _sympy.Integer(6),
          "N": _sympy.Integer(2)},
    "dU": {"H": _sympy.Integer(12),
           "C": _sympy.Integer(9),
           "O": _sympy.Integer(5),
           "N": _sympy.Integer(2)},
    "BICINE": {"H": _sympy.Integer(13),
               "C": _sympy.Integer(6),
               "N": _sympy.Integer(1),
               "O": _sympy.Integer(4)},
    "BisTris": {"H": _sympy.Integer(19),
                "C": _sympy.Integer(8),
                "O": _sympy.Integer(5),
                "N": _sympy.Integer(1)},
    "CAPS": {"H": _sympy.Integer(19),
             "S": _sympy.Integer(1),
             "C": _sympy.Integer(9),
             "O": _sympy.Integer(3),
             "N": _sympy.Integer(1)},
    "CHES": {"H": _sympy.Integer(17),
             "S": _sympy.Integer(1),
             "C": _sympy.Integer(8),
             "O": _sympy.Integer(3),
             "N": _sympy.Integer(1)},
    "HEPES": {"H": _sympy.Integer(18),
              "S": _sympy.Integer(1),
              "C": _sympy.Integer(8),
              "O": _sympy.Integer(4),
              "N": _sympy.Integer(2)},
    "MES": {"H": _sympy.Integer(13),
            "S": _sympy.Integer(1),
            "C": _sympy.Integer(6),
            "O": _sympy.Integer(4),
            "N": _sympy.Integer(1)},
    "MOPS": {"H": _sympy.Integer(15),
             "S": _sympy.Integer(1),
             "C": _sympy.Integer(7),
             "O": _sympy.Integer(4),
             "N": _sympy.Integer(1)},
    "TES_fa": {"H": _sympy.Integer(15),
               "S": _sympy.Integer(1),
               "C": _sympy.Integer(6),
               "O": _sympy.Integer(6),
               "N": _sympy.Integer(1)},
    "TRICINE": {"H": _sympy.Integer(13),
                "C": _sympy.Integer(6),
                "O": _sympy.Integer(5),
                "N": _sympy.Integer(1)},
    "TRIS": {"H": _sympy.Integer(11),
             "C": _sympy.Integer(4),
             "O": _sympy.Integer(3),
             "N": _sympy.Integer(1)},
    "Bu": {"H": _sympy.Integer(9),
           "C": _sympy.Integer(4)},
    "Cy": {"H": _sympy.Integer(11),
           "C": _sympy.Integer(6)},
    "Et": {"H": _sympy.Integer(5),
           "C": _sympy.Integer(2)},
    "Me": {"H": _sympy.Integer(3),
           "C": _sympy.Integer(1)},
    "Mes": {"H": _sympy.Integer(3),
            "C": _sympy.Integer(1),
            "O": _sympy.Integer(2),
            "S": _sympy.Integer(1)},
    "OSu": {"H": _sympy.Integer(4),
            "C": _sympy.Integer(4),
            "N": _sympy.Integer(1),
            "O": _sympy.Integer(3)},
    "Ph": {"H": _sympy.Integer(5),
           "C": _sympy.Integer(6)},
    "Pr": {"H": _sympy.Integer(7),
           "C": _sympy.Integer(3)},
    "Py": {"H": _sympy.Integer(4),
           "C": _sympy.Integer(5),
           "N": _sympy.Integer(1)},
    "Tol": {"H": _sympy.Integer(7),
            "C": _sympy.Integer(7)},
    "Tos": {"H": _sympy.Integer(7),
            "C": _sympy.Integer(7),
            "O": _sympy.Integer(2),
            "S": _sympy.Integer(1)},
    "Ac": {"H": _sympy.Integer(3),
           "C": _sympy.Integer(2),
           "O": _sympy.Integer(1)},
    "Alloc": {"H": _sympy.Integer(5),
              "C": _sympy.Integer(4),
              "O": _sympy.Integer(2)},
    "Bn": {"H": _sympy.Integer(7),
           "C": _sympy.Integer(7)},
    "Bzl": {"H": _sympy.Integer(8),
            "C": _sympy.Integer(7)},
    "Boc": {"H": _sympy.Integer(9),
            "C": _sympy.Integer(5),
            "O": _sympy.Integer(2)},
    "Bz": {"H": _sympy.Integer(5),
           "C": _sympy.Integer(7),
           "O": _sympy.Integer(1)},
    "DMT": {"H": _sympy.Integer(19),
            "C": _sympy.Integer(21),
            "O": _sympy.Integer(2)},
    "Fmoc": {"H": _sympy.Integer(11),
             "C": _sympy.Integer(15),
             "O": _sympy.Integer(2)},
    "MEM": {"H": _sympy.Integer(9),
            "C": _sympy.Integer(4),
            "O": _sympy.Integer(2)},
    "MOM": {"H": _sympy.Integer(5),
            "C": _sympy.Integer(2),
            "O": _sympy.Integer(1)},
    "Piv": {"H": _sympy.Integer(9),
            "C": _sympy.Integer(5),
            "O": _sympy.Integer(1)},
    "PMB": {"H": _sympy.Integer(9),
            "C": _sympy.Integer(8),
            "O": _sympy.Integer(1)},
    "SEM": {"H": _sympy.Integer(15),
            "Si": _sympy.Integer(1),
            "C": _sympy.Integer(6),
            "O": _sympy.Integer(1)},
    "TBDMS": {"H": _sympy.Integer(15),
              "Si": _sympy.Integer(1),
              "C": _sympy.Integer(6)},
    "TBS": {"H": _sympy.Integer(15),
            "Si": _sympy.Integer(1),
            "C": _sympy.Integer(6)},
    "TES": {"H": _sympy.Integer(15),
            "Si": _sympy.Integer(1),
            "C": _sympy.Integer(6)},
    "THP": {"H": _sympy.Integer(9),
            "C": _sympy.Integer(5),
            "O": _sympy.Integer(1)},
    "TMS": {"H": _sympy.Integer(9),
            "Si": _sympy.Integer(1),
            "C": _sympy.Integer(3)},
    "Tr": {"H": _sympy.Integer(14),
           "C": _sympy.Integer(19)},
    "Trt": {"H": _sympy.Integer(15),
            "C": _sympy.Integer(19)}
}
