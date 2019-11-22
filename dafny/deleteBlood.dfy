method Main() {
  var a1: array<string> := new string[5];
  a1[0], a1[1], a1[2], a1[3], a1[4]:= "A: 330ml", "AB: 250ml","A: 500ml","O: 1000ml", "B: 450ml";
  
  var a3 := deleteFromList(a1,2);
}

method deleteFromList(blood: array<string>, indexv: int) returns (result: array<string>)
requires blood != null
requires 0 <= indexv < blood.Length
ensures result != null
ensures 0 <= indexv <= result.Length
//This post condition ensured that the new array was exactly the same as the old array till the index was reached
//ensures result[0..indexv - 1] == blood[0 .. indexv - 1]
// This post condition ensured that the new array was storing one more than the old array in order to remove the deleted value successfully
//ensures result[indexv .. result.Length] == blood[indexv + 1 .. blood.Length]
{
  result := new string[blood.Length - 1];
  if (indexv != 0) {
    result[0] := blood[0];
  } 
  var i:= 0;
  while (i < result.Length) 
  invariant 0 <= i <= result.Length
  //These invariants have errors when trying to calculate whether the value was deleted successfully
  //This could be occuring because the value at index 0 could not be stored properly and thus the invariant was not being held successfully
  //invariant 0 <= i < indexv ==> result[i] == blood[i]
  //invariant indexv <= i < result.Length ==> result[i] == blood[i + 1]
  { 
    if (i < indexv) {
        result[i] := blood[i];
    } else {
        result[i] := blood[i+1];
    }
    i := i + 1;  
  }
    
      
}

