method hasLowBlood(m: array<int>, val: int, key: int) returns (b: bool)
	requires m != null
    ensures b <==> 0 <= key < m.Length && m[key] < val;
{
    if (0<= key < m.Length && m[key] < val)
		{
    	return true;
    }
    return false;
}



method Test()
{
  var e:array<int> := new int[6];
  e[0]:=2; e[1]:= 1; e[2]:=4;e[3]:= 1; e[4]:= 6; e[5] := 1;

  //when value is low
  var result := hasLowBlood(e,2, 1);
  assert result == true;

  //when value is high
  result := hasLowBlood(e,3,2);
  assert result == false;

  //when value is on edge
  result := hasLowBlood(e,1,5);
  assert result == false;

  //when index is out of range
  result := hasLowBlood(e,1,6);
  assert result == false;

  //when empty array
  var a:array<int> := new int[0];
  result:= hasLowBlood(a,1,2);
  assert result == false;
}
