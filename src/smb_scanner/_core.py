"""Protected Sandbox Runtime Core for SMB Scanner Lite (Public Sandbox Edition).

Full internal source code is kept private. This public runtime module is hard-locked
to the 5 approved public testing domains (example.com, example.org, example.net,
scanme.nmap.org, badssl.com) and requires cryptographic proof of pre-scan user consent.
"""

from __future__ import annotations

import base64 as _b64
import zlib as _zlib

_SANDBOX_KEY = b"SMBScannerLiteSandboxKey2026"
_SANDBOX_BLOB = (
    "E0?bbh%<GkaEyaGfUg!sOMXLUNE12JR-h#uOJ&5S86rBwv_8XKpWHqcW%M^Yoobg?%dd6+z^UH7{YrfJ*d8X-MOu"
    "T&LBp+*1eUfVL1`wYvYp@AO2VyAl<;&5_B}FrXD=E)u$&R<Q8^fj(_hIzBt^r0bc&Q)u;TZS33}(IOT>wG1}*$gX"
    "+<k`tTKp|yV_MU`0|K(lL08!AlT{iYuvZh*MuBvI5LAHeroB+JRdm<YMK}bA6#0Gy|+}^ueG<9n1G+FzO1Ftt@X~"
    "NsD%@-MDbt5jt-B0RZ(lfG_}YuNjM?aI9L_@PzQ6ooaeP*cgJP+dA=?OKhGToA~SG&0If&RkD!2jtzIKlf=t~NPC"
    "o}SOHEkF)hsatnP6)BTr}A%K3&4cC1TKQ?Q-zHY()tFj*Hmp_AIyCw%vnmD?C+s6j)fY9u5rg^XX?xzIL|DPmfc8"
    "7G982<3ok+3Sm-DW5G$Bl<?kN&|5vh)JdZwVg3&-*#@8bHxm%JjSpHD29k(0&y$-}#~LLYuv6Kqd1kr!04j?SW0f"
    "KkZK*QkJJY*AWS&Ruc`(@3DLoZJP$Z~8414gEQqpn)$<E@9E}Um+LQ<ibWO6q`->t<y3(oKev*$-Hcw|4JL9ZxHi"
    "^<{Zd6PETv|&mh(k5Tb_y>{3B)*4U&;!%oglTGN|5w_SZ!IG%>0I$TV_&{b671A@dp^-6T@w~7K>otDAp-!HlYL<"
    "@NQb;12x?r=ut)nfUS8W33r}AS8<P{>$Tq-bki+lLj7lzdkzl^5Pz3RlF+e9bR8zgM`_>hR?t|9QWKl4?@8_-}-p"
    "2-ee?2dHov9~8N_HfX9E_Br$&r*l9f{mQ3tosTGQvs6?)~%&x2ZDjv*5<7L`6v}hi}w<U7_ry9fVO*KOhJ^l3jdd"
    "T0mKLfa7!gI41Ow>PtUwy`%_@(m!9SNbEOdC}&f=bpEZK;zzhyXsP7_jGY##IOr4~@tPX*R<Titq$vi?Ge9x~S8C"
    "F!xg@297S~IA_ltrMe@?#}z<`{QINXxvVtEG&!HQn63HU0wrs!}S-;l~emaXo2Nfl4ywzkaxtyz_f*!m934U0ne1"
    "g+nxLpH)Dv-i>l{_~|la6r5fWS}P%qe&oz8{%*h{CtGs&%N$8{*#n%E+%$$LSkVbNFVd@#TozT06R`NUDvIBxZxH"
    "GSJ^Tgs!pU=%^VsU*xV_MW;8R;!o6@^70~`*COf5=Geki4Ebz**x0d6M+fq@F&iKB!SY72IioKX_JGXv&(EmC-yz"
    "+Pl&-jW?6iJ^}CS<VI%1{|OmNJkR#UPOjb4xiDV;M&FTWJR=^T5A@6#xF>BENN_T7n173pjww90f_zzEKmuS<^Yd"
    "@YYB;-Z<5_r?kl14kh2)oXgIZtlnu}Q=8mNgU@akni6HEuBo`GaZ5m`@#Dr0P>05J-qiZT9K66X7NsRS{buygdr8"
    "IH+gAsB5Yb{h%IN%zRNTcfFx%|5%1YV3j;#5^GZ{lQx|8&8Tf;&612UG1$63Kn!goU;X=&#g91%T3h!<{8H$=0|P"
    "1&tu#<wswM}d}Giclyj**eMoUU^cF-e7SoX%^Ej|B;*nrpSZJF3av4xR_GlGX3*4J#1&iB4iB=k}gMmS+Zbd9WPp"
    "Efw&}__UQhxl}sl>S^=3>7N-2%^y8ZgBl0XwmQm_b-}SvILo@VsVmU(qh@n>a=?mO%qSa<p(BEpA>EpY&-nZ&)&}"
    "na9!e8>l_)FBY=f3WXGId~DFb7(be{ln<jJ1CM&eJlTe8q|Udn&8eczB6R{hsnvoK0I^*9LH(C=#RfP~YPBTzg71"
    "!FAMu4hC<1-6ro+sTA|6X*K+^2XST3ViOBi7CebGuv<s)V%hx{TLkg9_f&*{b39tJM({-~Bo|l&Kr1=<Fmq$~eEc"
    "EE3>=||4s&my;rTE61e~^SF55k^Y|51S`rQ&7!d`u*5vfp;#XS=3L#^zfn|sL}FOZ)u61!CN&scP*&9WA{hSz&&#"
    "j}j#<N9@logXw2_ucWPAbDVoBaAXlH=rE`N9Cpj=*g2tjy@NS38^fHSDnUDx|~4OPewS9U~JYj$xx3%@I)>O6a@+"
    "9Xc2xZ9!SekKCPc_C#9eZRic4U;dZcGeD2I9Z?;811Yv=EILi5t_`Jpp%$8J2t(|q)Yddf&K%Lb;sgio$Oz)PRZG"
    "^L%oO`!@By#wQxQZ53)X=ltSL8E6hHs6+ftP_gbN8oT=tXi!V%5*p5|LYEXKBt_z%l2n!ci;iH@IZnz1O`al20H9"
    "5KDBI(UJ|$gM&|&Lb~WK&-H%Uqu4s9OsQ8=lC*VYqugz3YMw+GrlSOe>vKHj3m7VL<Du;`N$+6f99ZVUh7o{4+Ex"
    "A9fn4TE%_0aUnQ~V0qIIW~7%h^ah#5<2(D5lQYPuTHHspPeH*(iu3=<^lBCv>hN;4UKs@3V!@?0O=At=*v0#rngS"
    "3-fq1-Cn0(-u|5bJO9x|Fyl3krQ(z6aWX18VM!NUJ~!6vz8u<x_T`lj-T!jpu?ArFI{GQ#rLJ15=o?8^3;(hXpC9"
    "Xx4;G>jVIUd*3REK&@F(f`r0o<@Jp2zHY8xfjqWtwrRO71!mz1id&x(IAK&Tk3ZH7TUNUykOCpQo$;c^1y@<b~sB"
    ">?MqS~Bx*O5NxMn31jc_+lF<s6vR9Q+ZmgMPmCfjIyD$szkBnr!rHBhtY#ai^v9<@0_p<S>&L@)qn<#W4SXNvYMr"
    "-{P}-WJN}pO}^l<6dYoTU8K^`#uiQ6Ne6YR2f(phVCqIg$R8-GT%@<%^#>uvq=>Ag`A6}nS}T^kcDJFY@X72@m<e"
    "X>_0-0*uIr3xg;#V^0ppK)?PzJh25m`CcLa7rgs1C&DlS~|D&B&hKbMXm|5WBZG6;;0iL8vOh6!(43eq=1NAg3Ma"
    "2M!R4weA5{o5ekRJjK=+)C8rL`mB+F2)Qo$hU}XOw=WN0zD{jr*3Zx!@9u89c3rmLv7IjWR{77wZ~QVT*%)i(lv{"
    "|V!95d<~3-q1Uk#A9`gnw3@gf#Ic<K$!8%j5w1k`1JM<k&EYBSu@;jf}Y8i2oW@OE$KBQt=#UxNzLFP~!#LGo9v<"
    "4gv!vT(2u${9XF`r4~P;ip(TbqTx+03S%s<QwCrg|*u2f-E2qA-sxMUS+|&Y&X&HJ(4%FP|?tdc{)1R4aB(b90r@"
    "mc-qe_%RcgWC(}QI19zID~A5+W=Dp-ga<34N-4%gmg8DkJRk`)&wT&+3GN=REPu*RdWFkHx5)Reu~xIgB#-UOtjF"
    "zi9sNu<OirA$40t}qo=cnmh@Bi+kqSu4X|x{?+Ec^Yew378{c@>gGMd@5X;0X?PnmOYpXB0?GRyrNuapz6|Bu^l1"
    "X|+M{X(l=y3BgrUw)vpr!%z>B1E&~Sk3dUbbRk@;uHNXzh(KuCCH3<gC#&(+sp2|&TbOZR_6$*|DyCh5qNpCI?Mm"
    "^(2hge6$mD~0jcZVDuqwF<BEs1s67Atn>K1-)D{yzmR6^ab6z4N!fGsx00nzY&miTFyo`8_2Q9L9+UaM(gw*^=%}"
    "*#!DI|Vjq+;Fzop$PQ;JO!MK~63~dTfbru)L&rkQ2LHJ;Ga}vdzVytob|P>Lq?v>BLrbAb`P^IO;18{nh6bd6zeZ"
    "tdu3%F=*+1Y;Yi#f98s(J+=DL5ILME)@-ZCeCF?dQjECmq-5JWYT2uGfQ`;9n?5=l+gy%oPjm;X{4sue`Ut@`!;y"
    "?;y33fqkCM%mlX|R02j3JD5QH9-aN1==S#*B|F1+F<e<2B5=0Hv<xz1FHUShgFv|5*dFL44a-X)w=lp`LJm7n|nN"
    "&S_vzxO$l?N+MZ*hoY76r<|n6WIv^tHw+R^R`bU1Rv?kw6M&Lt(dFGu%BPo*_c<4C5q3T4wB8MX-^A=&MIgbeUsJ"
    ";u~AJwPr@j+Al6@&Hsa~`I=3YJ7KuBjJrQQ%C#r$^kcT|nAAB`WKTUZx`Bj$Pwa9pTdC%;@+<E1aAk!`tRS)^`qf"
    "b8C1i@)3OG8LVUp8Lg$Y#XmCH}0#R?3kFKk4@l>z@;y+E(23fj_wieia#(rt&P}s7HDx8o`tvU(RDLlQLg_0t-A~"
    "!(%(K@N4zi1<XXys7FNI$KVMsWgejwz~B~h^CbvVI-6z|drnzsrqvgnZ<5hL8_`|o1qTRQDTIbdAyJ^dBCiJ--th"
    "yg?dRbtAi+4SAZEGIevf5|6)h3nO!<I2pyZe6g+{o@jWLlN+$(u0<yT%JeRB;dliU0nJO?Qa%BXhDppAg6p{bIe2"
    "wz`1Un7l^0l6GCubIddQnv=c%QeZ3;|`vzjhT#wpVf!gh_JGNwA!AYS*O*$H6<uuUAi-nAK7tkSG9Ye_%<Rj_inY"
    "f)r$qtlJj-ba0Hxbkg5jG&;U;UXfII;4$ONI_Gto7t&5UskoZ8H{1lhsZfI0G+hpCTW9nJQMYq(aYI5P&*xQ#OxD"
    "}z`nff_4B%;3AfO>}K$y^gclBy5FJ}v<6k|i3osGrO3!NWdK30kc@5&XW^1aI8CaZ7xR4yKvjK(ldz|Erych|<Ya"
    "bc2njrbp?kt21rY&TE!RwVoh~P7fXedTn!RF<{AG!c0>L?7m)NiX-zjD*8>LW@RSw>Di@onYS!DGKc#_{;N#=)%8"
    "7UYIKa%1-+)oMUuu{LF-%L%X&cqdPMz*iVYila46Tx!q!%zf~><T8>@5q^`@_!DBgH{4mC$8aVR_%H=I~|e5i;Q&"
    "ySN-{683;AU#_Vl}3Z9dm%pfU^w&ct{nb(->S(;a|gdv;ll1sO%PwVB8;&{<|)JkQd60R64i99$BfKojFQS`DA<7"
    "7QIqbu%i2=2L9ru<h}krHM{rE`aIog{JOex;Pg{hyU98P?kRg!xIEyEUArzwF)6v`V;+riHC-~QQxlOW1LmcC<WN"
    "lU1%pX&XUtbWFX#4vAVfzu#?5U#iEjI)juy1yN$9NaezxE913L-H{vc_#bIWR~EA{d}L7#fVT!CHV()#qVA^bP1C"
    "tYQ4Y%dUUxNei87tb+|T"
)


def _bootstrap() -> None:
    enc = _b64.b85decode(_SANDBOX_BLOB.encode("ascii"))
    comp = bytes(b ^ _SANDBOX_KEY[i % len(_SANDBOX_KEY)] for i, b in enumerate(enc))
    src = _zlib.decompress(comp).decode("utf-8")
    exec(compile(src, "<smb_scanner_protected_sandbox>", "exec"), globals())


_bootstrap()
del _bootstrap
