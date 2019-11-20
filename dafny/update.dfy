class VampireSystem{
    var blood:array<string>
    ghost var gblood:array<string>;

    predicate Valid()
    reads this;
    { blood != null && gblood == blood }

    constructor (i:array<string>)
        requires i != null
    ensures Valid();
    modifies this;
    ensures gblood==blood==i;
    ensures blood != null
    { blood:= i; gblood := blood; }



    method updateBloodStatus(newdata:string, id:int)
    requires blood != null
    requires gblood != null
    requires Valid()
    requires 0 <= id < blood.Length
    requires 0 <= id < gblood.Length
    ensures Valid()
    modifies this.blood;
    ensures (forall i: int :: ( i == id && 0 <= i < blood.Length) ==> blood[i] == newdata);
    ensures (forall i: int :: (i != id && 0 <= i < blood.Length) ==> blood[i] == old(blood[i]));
    {
        var k: int := 0;
        while (k < blood.Length)
        decreases blood.Length - k
        invariant Valid()
        invariant 0 <= k < blood.Length
        invariant id >= k;
        invariant (forall i: int :: ( i == id && 0 <= i < k) ==> blood[i] == newdata);
    	invariant (forall i: int :: (i != id && 0 <= i < k) ==> blood[i] == old(blood[i]));
        {
        	if (k == id)
        	{
        		blood[k] := newdata;
        		return;
        	}
        	k := k + 1;
        }

    }

    method TestUpdateStatus()
    requires Valid();
    ensures Valid();
    {
	  var e:array<string> := new string[6];
	  e[0]:="tested"; e[1]:= "not-tested"; e[2]:="tested";e[3]:= "tested"; e[4]:= "not-tested"; e[5] := "tested";
	  var system := new VampireSystem(e);
	  system.updateBloodStatus("not-tested",2);
	  assert system.blood[2] == "not-tested";
      assert system.blood[0] == "tested";
      assert system.blood[1] == "not-tested";
      assert system.blood[3] == "tested";
      assert system.blood[4] == "not-tested";
      assert system.blood[5] == "tested";

      system.updateBloodStatus("not-tested",2);
	  assert system.blood[2] == "not-tested";
      assert system.blood[0] == "tested";
      assert system.blood[1] == "not-tested";
      assert system.blood[3] == "tested";
      assert system.blood[4] == "not-tested";
      assert system.blood[5] == "tested";

      system.updateBloodStatus("added",2);
	  assert system.blood[2] == "added";
      assert system.blood[0] == "tested";
      assert system.blood[1] == "not-tested";
      assert system.blood[3] == "tested";
      assert system.blood[4] == "not-tested";
      assert system.blood[5] == "tested";

      system.updateBloodStatus("tested",4);
	  assert system.blood[2] == "added";
      assert system.blood[0] == "tested";
      assert system.blood[1] == "not-tested";
      assert system.blood[3] == "tested";
      assert system.blood[4] == "tested";
      assert system.blood[5] == "tested";
	}

}
