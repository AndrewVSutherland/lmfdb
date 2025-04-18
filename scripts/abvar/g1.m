AttachSpec("/home/janeshi/Magma/magma.spec");
function IsogenyLabel(f,q)
// returns the LMFDB label of the isogeny class determined by f.
    g:=Degree(f) div 2;
    //q:=Integers() ! (Coefficients(f)[1]^(2/Degree(f)));
    str1:=Reverse(Prune(Coefficients(f)))[1..g];
    str2:="";
    for a in str1 do
        if a lt 0 then
            str2:=str2 cat "a" cat Base26Encode(-a) cat "_";
            else
            str2:=str2 cat Base26Encode(a) cat "_";
        end if;
    end for;
    str2:=Prune(str2);
    isog_label:=Sprintf("%o.%o.",g,q) cat str2;
    return isog_label;
end function;


// goal: enumerate all isomorphism class and collapse them together by isogeny classes.

// Note: twists of elliptic curves are elliptic curves isomorphic 
// over an algebraic closure but not over the base field. 

// J-invariants corresponds to isomorphism classes over algebraic closure, 
// so that's why enumerating the isomorphism classes over the smaller field F_q,
// we would like to get all twists of them.

// There's a theorem that says all twists of elliptic curves over F_q, (j inv not 0, 1728),
// the only twists are the quadratic twists. For j=0,1728, we can get quartic or sectic twists.


// Takes a prime power, and outputs an associative array,
// where the keys is the label, and the value is a canonical curve representing
// the isogeny class.

// Right now only works for characteristics not 2,3.

EnumerateIsogenyClassesG1 := function(q)

    k:=GF(q);

    // generate one representative for each j-invariant aside from 0, 1728,
    // and for each representative, generate all its twists.

    jInvReps := [EllipticCurveFromjInvariant(j) : j in k | not j in [k!0, k!1728]]; 
    allEllCurves := &cat[Twists(E): E in jInvReps];

    Pickc := function(F)
        // Choose the first nonsquare c in the field
        // where the order is determined by magma's default enumeration

        for x in F do 
            if not x eq 0 and not IsSquare(x) then 
                return x;
            end if;
        end for;
        return 0;

    end function;


    findIsomorphicRepresentative := function(E,c)

        // Returns an isomorphic model of the form 
        // y^2 = x^3 + Mx + M (if B/A is square)
        // or 
        // y^2 = x^3 + Mx + cM (if B/A is non-square)

        // by replacing (A,B) with (lambda^4*A, lambda^6*B)
        // where lambda = (Sqrt(B/A)^(-1)) if (B/A) is square,
        // (Sqrt((B/A)*c)^(-1)) otherwise

        // c is a non-square nonzero field element determined by Pickc

        E := WeierstrassModel(E);

        originalJinvariant:=jInvariant(E);

        A := Coefficients(E)[4];
        B := Coefficients(E)[5];

        assert not (A eq 0) and not (B eq 0);

        BoverA := B/A;

        Lambda := 1;

        if IsSquare(BoverA) then 
            Lambda := (Sqrt(BoverA))^(-1);
        else 
            Lambda := Sqrt((BoverA)^(-1)*(c));
        end if;

        canonicalE := EllipticCurve([0,0,0,Lambda^4*A, Lambda^6*B]);
        assert jInvariant(canonicalE) eq originalJinvariant;
        return canonicalE;

    end function;

    c := Pickc(k);

    // label to curves is dictionary, 
    // where the keys are labels, and values are 
    // sets of curves corresponding to the label.

    labelToCurves := AssociativeArray();

    for curve in allEllCurves do 

        label := IsogenyLabel(LPolynomial(curve),q);  
        if not label in Keys(labelToCurves) then 
            labelToCurves[label] := Set([]);
        end if;

        Include(~labelToCurves[label], findIsomorphicRepresentative(curve,c));
    end for;


    // Now, we deal with elliptic curves of j-invariants 0, 1728
    // To pick the representative for isomorphism class of a curve E,
    // since those curves is a one-parameter family
    // of the form y^2=x^3+Ax or y^2=x^3+B, 
    // the isomorphic curves are parametrized by lambda^4*A or lambda^6*B.
    // We pick the smallest number in this parametrization as representative.

    zeroJInvCurve := EllipticCurveFromjInvariant(k!0);
    zeroTwists:=Twists(zeroJInvCurve);

    l728JInvCurve := EllipticCurveFromjInvariant(k!1728);
    l728Twists:=Twists(l728JInvCurve);


    for curve in zeroTwists cat l728Twists do 

        E := WeierstrassModel(curve);

        if jInvariant(E) eq k!0 then 
            B:=Coefficients(E)[5];
            // pick smallest [lambda^4 * B] where we cycle all lambda in k
            repB := Min([lambda^4 * B : lambda in k| lambda ne 0]);
            E := EllipticCurve([0,0,0,0,repB]);
        else 
            A:=Coefficients(E)[4];
            // pick smallest [lambda^6 * A] where we cycle all lambda in k
            repA := Min([lambda^6 * A : lambda in k| lambda ne 0]);
            E := EllipticCurve([0,0,0,repA,0]);
        end if;

        label := IsogenyLabel(LPolynomial(E),q);  
        if not label in Keys(labelToCurves) then 
            labelToCurves[label] := Set([]);
        end if;

        Include(~labelToCurves[label], E);

    end for;


    //nice print function for associative array
    PrintAssociativeArray := procedure(AA)
        for k in Keys(AA) do
            print "k=",k," v:=",AA[k];
        end for;
    end procedure;

    PrintAssociativeArray(labelToCurves);

    /*


    // A helper function to determine the order 
    // of the curve based on the lexicographic order of the 
    // coefficients.
    CompareCurves := function(E1,E2)
        if Coefficients(E1) gt Coefficients(E2) then 
            return 1;
        else 
            return -1;
        end if;
    end function;

    // a helper function to return the "smallest"
    // curve with respect to the lexicographic ordering

    smallest := function(setOfCurves)
        curveList := [x: x in setOfCurves];
        Sort(~curveList, func<x, y| CompareCurves(x,y)>);
        return curveList[1];
    end function;


    // the dictionary that has keys as labels, and values as the 
    // smallest curve based on lexicographic ordering
    labelToCanonicalCurve := AssociativeArray();

    for label in Keys(labelToCurves) do
        labelToCanonicalCurve[label] := smallest(labelToCurves[label]);
    end for;

    PrintAssociativeArray(labelToCanonicalCurve);
    print "Total of ", #Keys(labelToCanonicalCurve), " isogeny classes.";

    */


    
    return labelToCanonicalCurve;
end function;


EnumerateIsogenyClassesG1(19);
EnumerateIsogenyClassesG1(19^2);

