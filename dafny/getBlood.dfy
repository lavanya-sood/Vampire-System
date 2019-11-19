predicate CorrectBlood(s: seq<int>, val: int)
{
    forall k ::0<= k < |s| ==> s[k] == val
}


method GetExactBloodAmount(a:array<int>,val:int) returns (r : seq<int>)
requires a != null
ensures CorrectBlood(r[..],val);
ensures |r| == multiset(a[..])[val];
{ 
var temp := new int[a.Length];
var i := 0;
var j := 0;
while (i < a.Length && j < temp.Length) 
invariant 0 <= i <= a.Length
invariant 0 <= j <= a.Length
invariant CorrectBlood(temp[..j],val)
invariant j == multiset(a[..i])[val]
{
  if (a[i] == val) {
    temp[j] := a[i];
    j := j + 1;
  }
  i := i + 1;
}
assert a[..] == a[..a.Length];
assert j == multiset(a[..])[val];
r := temp[..j];
}

method Main()
{
    var a : array<int> := new int[5];
    a[0]:= 500;a[1]:= 750;a[2] := 250;a[3]:=1000;a[4]:=250;
    var k := GetExactBloodAmount(a,250);
    assert |k| == multiset(a[..])[250];
    assert CorrectBlood(k,250);
     
    var a2 : array<int> := new int[1];
    a2[0]:= 500;
    k := GetExactBloodAmount(a2,250);
    assert |k| == 0;
    assert CorrectBlood(k,250);
}
    
