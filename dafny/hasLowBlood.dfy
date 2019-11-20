method hasLowBlood(m: array<int>, val: int, key: int) returns (b: bool)
	requires m != null
    ensures b <==> 0 <= key < m.Length && m[key] < val;
{
    if (0<= key < m.Length && m[key] < val){
    	return true;
    }
    return false;
}



method Test()
{
  var e:array<int> := new int[6];
  e[0]:=2; e[1]:= 1; e[2]:=4;e[3]:= 1; e[4]:= 6; e[5] := 1;

  var result := hasLowBlood(e,2, 1);
  assert result == true;

  result := hasLowBlood(e,3,2);
  assert result == false;

  result := hasLowBlood(e,1,5);
  assert result == false;

  result := hasLowBlood(e,1,6);
  assert result == false;
}
