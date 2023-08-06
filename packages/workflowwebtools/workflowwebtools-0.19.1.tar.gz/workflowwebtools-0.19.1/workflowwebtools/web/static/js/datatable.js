var theData = null;

Date.prototype.getWeekNumber = function(){
    var dayNum = this.getDay() ;
    if(dayNum == 0)
	dayNum = 7;

    var ddd = new Date( this.getFullYear() , this.getMonth() , this.getDate() , 0 , 0 , 0 );
    var dateOffset = (24*60*60*1000) * (dayNum-1);
    var ret = new Date(ddd.getTime() - dateOffset);
    return ret;
};
Date.prototype.getQuarter = function(){
    var m = this.getMonth();
    if( m < 3)
	return new Date( this.getFullYear() , 0 , 1 , 0 , 0 , 0 );
    else if( m < 6 )
	return new Date( this.getFullYear() , 3 , 1 , 0 , 0 , 0 );
    else if( m < 9 )
	return new Date( this.getFullYear() , 6 , 1 , 0 , 0 , 0 );
    else
	return new Date( this.getFullYear() , 9 , 1 , 0 , 0 , 0 );
};

function loadData(){
    if( theData != null )
	return theData;

    var jsonData = $.ajax({
	url: "/actionssummary",
	dataType: "json",
	async: false
    });

    google.charts.load('current', {'packages':['table']});
    theData = new google.visualization.DataTable();
    theData.addColumn( 'number' , 'index' );
    theData.addColumn( 'string' , 'user' );
    theData.addColumn( 'date' , 'Date' );
    theData.addColumn( 'date' , 'month' );
    theData.addColumn( 'date' , 'week' );
    theData.addColumn( 'date' , 'quarter' );

    for(var row in jsonData.responseJSON ){
	var dt = new Date( 1000*parseInt( jsonData.responseJSON[row][0] ) ) ;
	newRow = [ parseInt(row) , jsonData.responseJSON[row][1] , dt , new Date( dt.getFullYear() , dt.getMonth() , 1 , 0 , 0 , 0) , dt.getWeekNumber() , dt.getQuarter()  ];
	theData.addRow( newRow );
    }
    
    return theData;
};

function allUsers(){
    var users = google.visualization.data.group( loadData() , [1] );
    // var ret = [];
    // for( var i = 0 ; i < users.getNumberOfRows() ; i++ )
    // 	ret.push( users[i][0] );
    return users;
};

function getActionsPerUser( what ){ //what = date=2/week=4/month=3/quarter=5
    var distinctValues = loadData().getDistinctValues(1);

    var viewColumns = [what];
    var groupColumns = [];
    // build column arrays for the view and grouping
    for (var i = 0; i < distinctValues.length; i++) {
        viewColumns.push({
            type: 'number',
            label: distinctValues[i],
            calc: (function (x) {
                return function (dt, row) {
                    // return values of C only for the rows where B = distinctValues[i] (passed into the closure via x)
                    return (dt.getValue(row, 1) == x) ? 1 : 0;
                }
            })(distinctValues[i])
        });
        groupColumns.push({
            column: i + 1,
            type: 'number',
            label: distinctValues[i],
            aggregation: google.visualization.data.sum
        });
    }
    
    var view = new google.visualization.DataView(loadData());
    view.setColumns(viewColumns);
    //return view;
    // next, we group the view on column A, which gets us the pivoted data
    var pivotedData = google.visualization.data.group(view, [0], groupColumns);
    return pivotedData;
};
