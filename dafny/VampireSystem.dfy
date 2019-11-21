class VampireSystem{
    var blood:array<string>
     
    predicate Valid()
    reads this;
    { blood != null}

    constructor (i:array<string>)
    requires i != null;
    ensures Valid();
    ensures blood == i;
    ensures blood != null
    modifies this;
    { blood:= i; } 
    
    predicate DeliveredBlood(a: seq<string>)
    {
    forall k ::0 <= k < |a| ==> a[k] == "-"
    }

    method getDeliveredBlood() returns (result: seq<string>) 
    requires Valid(); ensures Valid();
    ensures DeliveredBlood(result[..]);
    ensures |result| == multiset(blood[..])["-"];
    { 
    var temp := new string[blood.Length];
    var i := 0;
    var j := 0;
    while (i < blood.Length && j < temp.Length) 
    invariant 0 <= i <= blood.Length
    invariant 0 <= j <= blood.Length
    invariant DeliveredBlood(temp[..j])
    invariant j == multiset(blood[..i])["-"]
    {
      if (blood[i] == "-") {
        temp[j] := blood[i];
        j := j + 1;
      }
      i := i + 1;
    }
    assert blood[..] == blood[..blood.Length];
    assert j == multiset(blood[..])["-"];
    result := temp[..j];
    }
        
       
    method updateBloodStatus(newdata:string, id:int)
    requires blood != null
    requires Valid()
    requires 0 <= id < blood.Length
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
    
    method updateInputDate(newdate:string, id:int)
    requires blood != null
    requires Valid()
    requires 0 <= id < blood.Length
    ensures Valid()
    modifies this.blood;
    ensures (forall i: int :: ( i == id && 0 <= i < blood.Length) ==> blood[i] == newdate);
    ensures (forall i: int :: (i != id && 0 <= i < blood.Length) ==> blood[i] == old(blood[i]));
    {
    var k: int := 0;
    while (k < blood.Length)
    decreases blood.Length - k
    invariant Valid()
    invariant 0 <= k < blood.Length
    invariant id >= k;
    invariant (forall i: int :: ( i == id && 0 <= i < k) ==> blood[i] == newdate);
	  invariant (forall i: int :: (i != id && 0 <= i < k) ==> blood[i] == old(blood[i]));
    {
    	if (k == id)
    	{
    		blood[k] := newdate;
    		return;
    	}
    	k := k + 1;
    }
    }
    
    
    method updateDeliveredStatus(id :int,newdata:string)
    requires blood != null
    requires Valid()
    requires 0 <= id < blood.Length
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
    
    method getRequest() returns (r:array<string>)
    requires Valid();
    ensures Valid();
    ensures fresh(r);
    ensures r != null;
    ensures r.Length == 5;
    ensures r[0]== "blood C";
    ensures r[1]== "blood A";
    ensures r[2]== "blood B";
    ensures r[3]== "blood B";
    ensures r[4]== "blood O";
    {
        r := new string[5]; 
        r[0]:= "blood C";r[1]:= "blood A";
        r[2] := "blood B";r[3]:="blood B";r[4]:="blood O";  
    }
    
  
}

// testing methods and class
method Main()
{    
    var a : array<string> := new string[2];
    a[0]:= "B";a[1]:="A";
    var v := new VampireSystem(a);
    
    // test getDeliveredBlood method
    var answer := v.getDeliveredBlood();
    assert |answer| == multiset(a[..])["-"];
    assert v.DeliveredBlood(answer);
 
    // test update methods
    // since the update funcs are the same
    // only testing updateBloodStatus is done extensively
      
    var e:array<string> := new string[6];
    e[0]:="tested"; e[1]:= "not-tested";
    e[2]:="tested";e[3]:= "tested"; 
    e[4]:= "not-tested"; e[5] := "tested";
    var system := new VampireSystem(e);
    system.updateBloodStatus("not-tested",2);
    assert system.blood[2] == "not-tested";
    assert system.blood[0] == "tested";
    assert system.blood[1] == "not-tested";
    assert system.blood[3] == "tested";
    assert system.blood[4] == "not-tested";
    assert system.blood[5] == "tested";
    
    // test updating the value to the same value
    system.updateBloodStatus("not-tested",2);
    assert system.blood[2] == "not-tested";
    assert system.blood[0] == "tested";
    assert system.blood[1] == "not-tested";
    assert system.blood[3] == "tested";
    assert system.blood[4] == "not-tested";
    assert system.blood[5] == "tested";
    
    // test updating the same blood id again
    system.updateBloodStatus("added",2);
    assert system.blood[2] == "added";
    assert system.blood[0] == "tested";
    assert system.blood[1] == "not-tested";
    assert system.blood[3] == "tested";
    assert system.blood[4] == "not-tested";
    assert system.blood[5] == "tested";
    
    // test updating other blood id
    system.updateBloodStatus("tested",4);
    assert system.blood[2] == "added";
    assert system.blood[0] == "tested";
    assert system.blood[1] == "not-tested";
    assert system.blood[3] == "tested";
    assert system.blood[4] == "tested";
    assert system.blood[5] == "tested";
	
	 // check updateInputDate method
	  var e2 : array<string> := new string[6];
    e2[0]:=""; e2[1]:= "2019-08-12"; 
    e2[2]:="";e2[3]:= "2019-08-02"; 
    e2[4]:= "2019-08-10"; e2[5] := "";
    system := new VampireSystem(e2);
    system.updateInputDate("2019-10-11",5);
    assert system.blood[0] == "";
    assert system.blood[1] == "2019-08-12";
    assert system.blood[2] == "";
    assert system.blood[3] == "2019-08-02";
    assert system.blood[4] == "2019-08-10";
    assert system.blood[5] == "2019-10-11";
    
    // check updateDeliveredStatus method
    var e3 : array<string> := new string[6];
    e3[0]:=""; e3[1]:= "no"; 
    e3[2]:="";e3[3]:= ""; 
    e3[4]:= "yes"; e3[5] := "no";
    system := new VampireSystem(e3);
    system.updateDeliveredStatus(2,"yes");
    assert system.blood[2] == "yes";
    assert system.blood[0] == "";
    assert system.blood[1] == "no";
    assert system.blood[3] == "";
    assert system.blood[4] == "yes";
    assert system.blood[5] == "no";
    
    // test getRequest method
    var r := v.getRequest();     
    assert r.Length == 5;
    assert r != null;
    assert r[0] == "blood C";
    assert r[1] == "blood A";
    assert r[2] == "blood B";
    assert r[3] == "blood B";
    assert r[4] == "blood O";
    
}
