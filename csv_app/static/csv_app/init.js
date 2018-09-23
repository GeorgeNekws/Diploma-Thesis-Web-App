
/************************************** P5.JS *****************************************************/
var mirnas = []; //put objects created in list   -- clear these lists every time, check the mirna list for example
//var region_info = json[2]; //u can use this variable instead of region_info

var superman;
var mirnaDiv;

var canvas_x = 50;
var canvas_y = 280;
var canvas_width;
var canvas_height;
var resol_factor1;
var resol_factor2 = 1.067185;

/*--------------------------------------------------------------------------------------------*/

function setup() {
  console.log('WindowWidth '+windowWidth);
  console.log('WindowHeight '+windowHeight);
  resol_factor1 = 1366 / windowWidth;

  console.log('factor1 : '+resol_factor1);
  console.log('factor2 : '+resol_factor2);

  canvas_width = Math.round(windowWidth/resol_factor2); //canvas size depending screen size
  console.log('Canvas Width : '+canvas_width);
  canvas_height = 1500;

  noLoop();
}

/*--------------------------------------------------------------------------------------------*/

function canvas_position(){
  var canvas = createCanvas(canvas_width, canvas_height);  //(1280,1500)
  canvas.position(canvas_x, canvas_y); //upper left point of canvas to position (x,y)=(50,250)
  console.log(windowWidth);
  background('yellow');
  clear();
}

/*--------------------------------------------------------------------------------------------*/

function mousePressed(){
  $('.removeDivFamilies').remove();
  for(var i=0; i<mirnas.length; i++){
    mirnas[i].clicked(mouseX,mouseY);
  }
}

/*--------------------------------------------------------------------------------------------*/

// Before families used:
// function draw_the_miRNAs(json,new_length,alpha){
//   for(i = 4; i < json.length; i++){ //variable : i , starts counting from 3 , because json[0]=general info, json[1]=chr info, region_info= regions info(utr,cds,exons...)
//     m = new Mirna(json[i], new_length, i , alpha);
//     mirnas.push(m);
//     m.draw_mirna();
//   }
// }

/*--------------------------------------------------------------------------------------------*/

function draw_the_miRNAs(json,new_length,alpha){
  superman = select('#superman-id');
  mirnaDiv = createDiv('');   //scroll div window

  mirnaDiv.position(0 , 740);
  mirnaDiv.id('mirnaID-div');
  mirnaDiv.addClass('removeComponents');

  //mirnaDiv.style('height' , '800px');
  console.log(windowHeight);
  //SCROLL HEIGHT
  var scroll_div_height = 870/(957/windowHeight);
  scroll_div_height = ''+scroll_div_height+'px';
  console.log(scroll_div_height);
  mirnaDiv.style('height' , scroll_div_height);
  //SCROLL WIDTH
  var scroll_div_width = 1900/(1920/windowWidth);
  scroll_div_width = ''+scroll_div_width+'px';
  console.log(scroll_div_width);
  mirnaDiv.style('width' , scroll_div_width);

  mirnaDiv.style('white-space' , 'nowrap');
  mirnaDiv.style('overflow' , 'hidden');
  mirnaDiv.style('text-overflow' , 'clip');
  mirnaDiv.style('overflow-x' , 'auto');
  mirnaDiv.style('overflow-y' , 'auto');
  mirnaDiv.style('border','0px solid #000');

  families = json[3]
  // console.log('FAMILIES');
  // console.log(families);
  mirnas = [] //clear the list for every new USER Search , do the same with the other lists
  for(i = 0; i < families.length; i++){ //variable : i , starts counting from 3 , because json[0]=general info, json[1]=chr info, region_info= regions info(utr,cds,exons...)
    m = new Mirna(families[i], new_length, i , alpha);
    mirnas.push(m);
    m.draw_mirna();
  }
}

/*--------------------------------------------------------------------------------------------*/

function draw_the_transcipt_regions(region_info, alpha, new_length){
  //Draw the 3'utr , 5'utr , cds , exon regions as rectangulars on the transcript.
  for (var i=0; i<region_info.length;i++){
    if(region_info[i].three_utr_start != 0){
      //call class
      r = new Rect_region(region_info[0].strand, region_info[i].three_utr_start, region_info[i].three_utr_stop, 'red', alpha, new_length , 0);
      r.draw_region();
    }
    if(region_info[i].five_utr_start != 0){
      //call class
      r = new Rect_region(region_info[0].strand, region_info[i].five_utr_start, region_info[i].five_utr_stop, 'green', alpha, new_length , 0);
      r.draw_region();
    }
    if(region_info[i].genomic_coding_start != 0){
      //call class
      r = new Rect_region(region_info[0].strand, region_info[i].genomic_coding_start, region_info[i].genomic_coding_stop, 'blue', alpha, new_length , 0);
      r.draw_region();
    }
  }
  //console.log('done Region');
}

/*--------------------------------------------------------------------------------------------*/

function draw_all_the_transcipt_regions(region_info, alpha, new_length){
  //Draw the 3'utr , 5'utr , cds regions as rectangulars on the transcript.
  for (var i=0; i<region_info.length;i++){
    if(region_info[i].three_utr_start != 0){
      //call class
      r = new Rect_region(region_info[0].strand, region_info[i].three_utr_start, region_info[i].three_utr_stop, 'red', alpha, new_length , 1);
      r.draw_region();
    }
    if(region_info[i].five_utr_start != 0){
      //call class
      r = new Rect_region(region_info[0].strand, region_info[i].five_utr_start, region_info[i].five_utr_stop, 'green', alpha, new_length , 1);
      r.draw_region();
    }
    if(region_info[i].genomic_coding_start != 0){
      //call class
      r = new Rect_region(region_info[0].strand, region_info[i].genomic_coding_start, region_info[i].genomic_coding_stop, 'blue', alpha, new_length , 1);
      r.draw_region();
    }
  }
  //console.log('done Region');
}

/*--------------------------------------------------------------------------------------------*/

function draw_the_transcript(data, user_input){
  //Draw the given by user Transcript as a line
  noStroke();
  textSize(9);

  var name_transcr= createP(user_input);
  name_transcr.position(canvas_width/2 - 40 , canvas_y + 230);
  name_transcr.addClass('removeComponents');
  name_transcr.style('text-align','center');
  name_transcr.style('padding','25px');
  name_transcr.style('font-size','13px');

  fill('black');

  //console.log(data.gene_strand);

  if(data.gene_strand == '+'){
    //console.log('sin');
    text('5-UTR',20/resol_factor1,290);
    text('3-UTR',1200/resol_factor1,290);
  }
  else{
    //console.log('plin');
    text('3-UTR',20/resol_factor1,290);
    text('5-UTR',1200/resol_factor1,290);
  }

  text(data.transcript_start,10/resol_factor1,320);
  text(data.transcript_stop,1200/resol_factor1,320);
  text(data.min,10/resol_factor1,430);                          //for partial transcript
  text((data.min+data.new_length-1),1200/resol_factor1,430);    //i subtract 1 from new_length, because in views.py i add 1 to calculate a distance , but here i need the number 'max'

  stroke('black');
  strokeWeight(1);
  line(30/resol_factor1,440,1210/resol_factor1,440);  //for partial transcript
  line(30/resol_factor1,437,30/resol_factor1,443);
  line(1210/resol_factor1,437,1210/resol_factor1,443);

  line(30/resol_factor1,300,1210/resol_factor1,300);  //for whole transcript
  line(30/resol_factor1,297,30/resol_factor1,303);
  line(1210/resol_factor1,297,1210/resol_factor1,303);
}

/*--------------------------------------------------------------------------------------------*/

function draw_the_gene(gene){

  //Draw the Whole gene as a line
  stroke('black');
  strokeWeight(1);
  line(40/resol_factor1,170,1200/resol_factor1,170);

  //with arrows describing its strand
  //arrows to the left
  if(gene.gene_strand == '-'){
    for(i=0;i<=57;i++){
      line((40 + 20*i)/resol_factor1 , 170, (40 + 20*i + 4)/resol_factor1 , 167 );
      line((40 + 20*i)/resol_factor1 , 170, (40 + 20*i + 4)/resol_factor1 , 173 );
    }
    fill('black');
    noStroke();
    textSize(9);
  }
  //arrows to the right
  else{
    for(i=1;i<=58;i++){
      line((40 + 20*i)/resol_factor1 , 170, (40 + 20*i - 4)/resol_factor1 , 167 );
      line((40 + 20*i)/resol_factor1 , 170, (40 + 20*i - 4)/resol_factor1 , 173 );
    }
    fill('black');
    noStroke();
    textSize(9);
  }
  text(gene.gene_start , 10/resol_factor1 , 190);
  text(gene.gene_stop , 1200/resol_factor1 , 190);

  //gene name, geneId,
  var name_gene = createP(gene.gene_name + ' (' + gene.gene_identifier + ' )');
  name_gene.position(canvas_width/2 - 80 , canvas_y + 100);
  name_gene.addClass('removeComponents');
  name_gene.style('text-align','center');
  name_gene.style('padding','25px');
  name_gene.style('font-size','13px');
}

/*--------------------------------------------------------------------------------------------*/

function draw_the_chromosome(gene , chr_bands){
  //var chr_bands = bands;
  var chromo_len;
  var gene_location ;

  chromo_len = chr_bands[chr_bands.length-1].bp_stop  //length of chromosome not in iscn as first , but in bp

  //Draw the chromosome bands
  for(var i=0; i<chr_bands.length; i++){
    b = new cytoBand(chr_bands[i], chromo_len);
    b.draw_band();
  }

  //Draw the Chromosome-Name next to the chromosome
  var name_chr = createP("chr: " + gene.gene_chromosome+ ' ('+chr_bands[0].arm+chr_bands[0].band+'-'+chr_bands[chr_bands.length-1].arm+chr_bands[chr_bands.length-1].band+')');
  name_chr.position(canvas_width/2 - 45 , canvas_y-30 );
  name_chr.addClass('removeComponents');
  name_chr.style('text-align','center');
  name_chr.style('padding','25px');
  name_chr.style('font-size','13px');

  // Draw the Gene as a line over the chromosome
  //toDO : scale, bps , length of gene like http://genome-euro.ucsc.edu/cgi-bin/hgTracks?db=hg38&lastVirtModeType=default&lastVirtModeExtraState=&virtModeType=default&virtMode=0&nonVirtPosition=&position=chr8%3A80628451%2D80874781&hgsid=228224761_ab1Ij5AZhEccKIgWVGY6yM6zHdVH
  gene_location = Math.round((gene.gene_start - chr_bands[0].bp_start ) / (chr_bands[chr_bands.length-1].bp_stop - chr_bands[0].bp_start) * (1200-40) + 40) ;
  stroke("red");
  strokeWeight(2);
  line(gene_location/resol_factor1,34,gene_location/resol_factor1,60);

  //console.log("GENE INFO NOW");
  //console.log('GENE START '+gene.gene_start);

  //console.log(chr_bands[(chr_bands.length)-1].bp_stop);
  //console.log(chr_bands[0].bp_start);
  //console.log(gene_location);
}

/*--------------------------------------------------------------------------------------------*/

class cytoBand{
  //constructor(stain, density, arm, band_start, band_stop){
  constructor(chr_bands , chromo_len){
    this.chromo_len = chromo_len  ;

    this.color_band = 'white';
    this.band = chr_bands.band;
    this.stain = chr_bands.stain;
    this.density = chr_bands.density;
    this.arm = chr_bands.arm;
    this.band_start = Math.round((chr_bands.bp_start / this.chromo_len) * (1200-40) + 40); //this is where each band starts
    this.band_stop = Math.round((chr_bands.bp_stop / this.chromo_len) * (1200-40) + 40);   //this is where each band stops
    this.middle_of_band =(this.band_stop+this.band_start)/2;
    this.band_width = this.band_stop - this.band_start;
  }

  draw_band(){
    var chr_y = 40; //draw the chr in heigt 'chr_y' relative to canvas

    if(this.stain == 'gneg'){
      noStroke();
      fill(255);
      rect(this.band_start/resol_factor1, chr_y, this.band_width/resol_factor1, 14);
      this.color_band = 'black';
    }
    else if(this.stain == 'gpos'){
      if(this.density == 25){
        noStroke();
        fill('LightGray');
        rect(this.band_start/resol_factor1, chr_y, this.band_width/resol_factor1, 14);
        this.color_band = 'black';
      }
      else if(this.density == 50){
        noStroke();
        fill('DarkGray');
        rect(this.band_start/resol_factor1, chr_y, this.band_width/resol_factor1, 14);
      }
      else if(this.density == 75){
        noStroke();
        fill("DimGray");
        rect(this.band_start/resol_factor1, chr_y, this.band_width/resol_factor1, 14);
      }
      else if(this.density == 100){
        noStroke();
        fill(40);
        rect(this.band_start/resol_factor1, chr_y, this.band_width/resol_factor1, 14);
      }
    }
    else if(this.stain == 'acen'){
      if(this.arm == 'p'){
        noStroke();
        fill('#ff3333');
        triangle(this.band_start/resol_factor1,(chr_y-1), this.band_start/resol_factor1,(chr_y-1)+15, this.band_stop/resol_factor1,(chr_y-1)+7);

        //chromosome contour 1 - before centromere
        stroke('black');
        line((this.band_start-1)/resol_factor1, (chr_y-1), 40/resol_factor1, (chr_y-1));
        line(40/resol_factor1, (chr_y-1), 40/resol_factor1, (chr_y-1)+15);
        line(40/resol_factor1, (chr_y-1)+15, (this.band_start-1)/resol_factor1, (chr_y-1)+15);
      }
      else{
        noStroke();
        fill('#ff3333');
        triangle(this.band_stop/resol_factor1,(chr_y-1), this.band_stop/resol_factor1,(chr_y-1)+15, this.band_start/resol_factor1,(chr_y-1)+7);
        //chromosome contour , write down the coordinates to paint later after the end of loop
        stroke('black');
        line(this.band_stop/resol_factor1,(chr_y-1),1200/resol_factor1,(chr_y-1));
        line(1200/resol_factor1,(chr_y-1),1200/resol_factor1,(chr_y-1)+15);
        line(1200/resol_factor1,(chr_y-1)+15,this.band_stop/resol_factor1,(chr_y-1)+15);
      }
    }
    else if(this.stain == 'gvar'){
      noStroke();
      fill('#283747');
      rect(this.band_start/resol_factor1, chr_y, this.band_width/resol_factor1, 14);
    }
    else if(this.stain == 'stalk'){
      noStroke();
      fill('#e59866');
      rect(this.band_start/resol_factor1, chr_y, this.band_width/resol_factor1, 14);
    }

    //arm and band text onto the bands
    if(this.band_width >= 32 && this.stain != 'acen'){
      textSize(8);
      noStroke();
      if(this.color_band == 'white'){
        fill(255);
      }
      else{
        fill(0);
      }
      text(this.arm+this.band, (this.band_start+3)/resol_factor1, chr_y+10 );
    }
  }
}

/*--------------------------------------------------------------------------------------------*/

class Mirna{
  constructor(mirna_info, new_length, y, alpha){
    this.begin = mirna_info.bind_start;
    this.end = mirna_info.bind_stop;
    this.new_length = new_length;
    this.mirna_name = mirna_info.mirna_name;
    this.alpha = alpha;

    //pop-up info
    this.mirna_sequence = mirna_info.mirna_conn__mirna_sequence;
    this.mirna_seed = mirna_info.mirna_conn__mirna_seed;
    this.mirna_id = mirna_info.mirna_conn__mirna_id;
    this.bind_site = mirna_info.bind_site;
    this.bind_type = mirna_info.bind_type;
    //this.score = parseFloat(mirna_info.score).toPrecision(3);
    this.score = mirna_info.score.toString().slice(0,5); // method toPrecision was rounding the number so i dont use it

    this.family = mirna_info.mirna_conn__mirna_family;
    this.bool_family = mirna_info.merged_in_family;

    this.y = 2+13*i; //the height where mirnas start to be drawn
    this.pressed = 0;

    this.span_tooltip = createElement('ul', '');
    //this.l0 = createElement('li' , 'microRNA: '+this.mirna_name);
    this.l1 = createElement('li' , 'MIMAT ID: '+this.mirna_id);
    this.l2 = createElement('li' , 'Seed sequence: '+this.mirna_seed);
    this.l3 = createElement('li' , 'Bind Site: '+this.bind_site);
    this.l4 = createElement('li' , 'Bind Type: '+ this.bind_type);
    this.l5 = createElement('li' , 'miTG Score: '+this.score);
    this.l6 = createElement('li' , 'Bind Start: ' +this.begin);
    this.l7 = createElement('li' , 'Bind Stop: ' +this.end);
    //this.span_tooltip.child(this.l0);
    this.span_tooltip.child(this.l1);
    this.span_tooltip.child(this.l2);
    this.span_tooltip.child(this.l5);
    this.span_tooltip.child(this.l6);
    this.span_tooltip.child(this.l7);
    this.span_tooltip.child(this.l3);
    this.span_tooltip.child(this.l4);

    this.rect_div2;
    //this.rect_div2_width ;
    this.text;
    this.text_width;
  }
  draw_mirna(){
    //console.log(this.mirna_name + ' : ' +this.begin + '  -  ' + this.family);
    // console.log('mirna start = '+ this.begin);
    // console.log('mirna stop = '+ this.end);
    //console.log((parseInt(this.begin)) + '  -   '+ this.alpha);
    this.begin = ((parseInt(this.begin)-this.alpha ) / this.new_length)*(1200-40) +40 ;   //parseInt(this.begin) return the first coordinate, when i have the occasion parseInt(4343;211) -->4343   (#LABEL : semicolon)
    //console.log(this.mirna_name + ' ' +this.begin);
    // console.log('mirna start = '+ this.begin);
    // console.log('mirna stop = '+ this.end);

    this.rect_div = createDiv('');

    mirnaDiv.child(this.rect_div);

    this.rect_div.addClass('removeComponents');
    this.rect_div.style('width','8px');
    this.rect_div.style('height','8px');
    this.rect_div.style('border-style','none');
    //console.log(this.score);
    if(this.score <= 1.0 && this.score >= 0.9){
      this.rect_div.style('background-color', 'red');
    }
    else if(this.score < 0.9 && this.score >= 0.8){
      this.rect_div.style('background-color', 'rgb(255, 102, 102)');
    }
    else if(this.score < 0.8 && this.score >= 0.7){
      this.rect_div.style('background-color', 'rgb(255, 128, 0)');
    }
    else if(this.score < 0.7 && this.score >= 0.6){
      this.rect_div.style('background-color', 'rgb(255, 178, 102)');
    }
    else{
      this.rect_div.style('background-color', 'rgb(255, 255, 0)');
    }

    this.rect_div.position((Math.round(this.begin)/resol_factor1) + canvas_x, (this.y));

    this.rect_div.id('tooltip');
    this.span_tooltip.id('tooltiptext');
    (this.span_tooltip).parent(this.rect_div);


    //Display mirna names
    fill('black');
    noStroke();
    textSize(6);
    if( this.bool_family == 1){
      //textStyle(BOLD);
      //this.text = text(this.family, (Math.round(this.begin)/resol_factor1)+10, (this.y));
      this.text = createP(this.family);
      this.text.style('font-weight' , 'bold')
      //this.rect_div2_width =  ((this.family).length * 6) + 10;
      this.text_width = ((this.family).length * 6) + 10;
    }
    else{
      //textStyle(NORMAL);
      //this.text = text(this.mirna_name, (Math.round(this.begin)/resol_factor1)+10, (this.y));
      this.text = createP(this.mirna_name);
      //this.rect_div2_width =  ((this.mirna_name[0]).length * 6) + 10;
      this.text_width = ((this.mirna_name[0]).length * 6) + 10;
    }

    this.text.style('font-size','10px');
    this.text.position((Math.round(this.begin)/resol_factor1)+10+canvas_x, (this.y)-3);   //text is drawn by x=+ 10 from the start of the rectangular this.y-11+canvas_y

    this.text.addClass('removeComponents');

    //this.rect_div2_width = "" + this.rect_div2_width +'px';
    mirnaDiv.child(this.text);

    return this.y;
  }


  //event handler edw mesa
  clicked(mx,my){
    var el = document.getElementById('mirnaID-div');
    // get scroll position in px
    //console.log( el.scrollTop);
    var scroll = el.scrollTop;
    var scroll2 = el.scrollLeft;  // mx <= (Math.round(this.begin)/resol_factor1)+8+this.text_width - scroll2  --> because if i scroll right and i press on text i have to circle all the mirna families

    if(scroll){
      //console.log("SCROLL EXISTS !!!!!");
    }
    else{
      //console.log("SCROLL DOES NOT EXISTS !!!!!!");
    }

    //470 is the hight of the first mirna from the start of canvas
    if( (my <= this.y-scroll+470) && (my >= (this.y)-8-scroll+470) && (mx <= (Math.round(this.begin)/resol_factor1)+8+this.text_width-scroll2) &&  (mx >= (Math.round(this.begin)/resol_factor1)+8-scroll2) ){ //clicking on text
      //console.log(this);
      //console.log(this.y);
      //console.log(this.y+scroll);
      $('.removeDivFamilies').remove();   //i remove the previous shown rects , so i can show up the new ones

      for(var i=0; i<mirnas.length;i++){    //for each mirna component that i have drawn , i check if it belongs to the same family with the one that was clicked

        if(mirnas[i].family == this.family){
           mirnas[i].rect_div2 = createDiv('');
           mirnas[i].rect_div2.addClass('removeDivFamilies');

           mirnas[i].rect_div2.style('width', "" + mirnas[i].text_width +'px');
           mirnas[i].rect_div2.style('height','13px');
           mirnas[i].rect_div2.style('border','1px solid #000');

           mirnas[i].rect_div2.position((Math.round(mirnas[i].begin)/resol_factor1) +9+ canvas_x, (mirnas[i].y)-2); //(mirnas[i].y)-2+canvas_y-scroll+460);
           mirnas[i].text.child(mirnas[i].rect_div2);   //nomizw douleuei kai xwris auto
           mirnaDiv.child(mirnas[i].rect_div2);
        }
      }
    }
  }
}

/*--------------------------------------------------------------------------------------------*/

class Rect_region{
  constructor(strand, start, stop, color, alpha, new_length, all_regions){
    this.new_length = new_length;
    this.alpha = alpha;
    this.all_regions = all_regions;

    this.start = start;
    this.stop = stop;
    this.l;
    this.color = color;
    this.strand = strand;
  }

  draw_region(){

    this.span_tooltip = createElement('ul', '');
    if (this.strand == 1){
      this.l1 = createElement('li' , 'Region Start: '+this.start);
      this.l2 = createElement('li' , 'Region Stop: '+this.stop);
    }
    else{
      this.l1 = createElement('li' , 'Region Start: '+this.stop);
      this.l2 = createElement('li' , 'Region Stop: '+this.start);
    }
    this.span_tooltip.child(this.l1);
    this.span_tooltip.child(this.l2);

    this.start = Math.round(( (this.start -this.alpha ) / (this.new_length) ) * (1200-40) +40) ; //an valw anti gia 40 , to 30 tote to rect region 8a arxisei apo 1h ka8eti grammi tou transcrip , ekei pou leei kai tin sintetagmeni arxis
    this.stop = Math.round(( (this.stop-this.alpha ) / (this.new_length) ) * (1200-40) +40) ;

    //console.log('new start region ' + this.start);
    //console.log('new stop region ' + this.stop);
    //console.log('diafora '+ (this.stop-this.start));

    if(this.stop-this.start+1<2){   //if the new calculated region len is smaller than 2px then assign it the value of 2px
      this.l = '2px';
    }
    else{
      this.l = ((this.stop - this.start+1) / resol_factor1).toString()+'px';
    }

    this.rect_div = createDiv('');
    this.rect_div.addClass('removeComponents');
    this.rect_div.style('width',this.l);
    this.rect_div.style('height','7px');

    if(this.color == 'red'){
      this.rect_div.style('background-color', 'red');
    }
    else if (this.color == 'green') {
      this.rect_div.style('background-color', 'green');
    }
    else{ //color: blue
      this.rect_div.style('background-color', 'blue');
    }

    if(this.all_regions == 1){
      this.rect_div.position((Math.round(this.start)/resol_factor1)+canvas_x, canvas_y+300-3);
    }
    else{
                                                                                                  //440 is the height 'y', where i have drawn the transcript
      this.rect_div.position((Math.round(this.start)/resol_factor1)+canvas_x, canvas_y+440-3);    // '-3': so the rect region is shown on the transcript line
    }

    //console.log('LLLLL');
    //console.log(this.l);
    //console.log('start paint :' +(Math.round(this.start)/resol_factor1));

    this.rect_div.id('tooltip-region');
    this.span_tooltip.id('tooltiptext-region');
    (this.span_tooltip).parent(this.rect_div);
  }
}

/*--------------------------------------------------------------------------------------------*/

function show_statistics(num_of_total_mirnas , data){
  // Get the modal
  //console.log(data);
  //var modal_body = document.getElementById('modal-bd');
  var left_modal_body = document.getElementById('modal1');
  var modal = document.getElementById('myModal');

  // Fill the modal-body with the statistics
  $('#modal1').append('- Total MREs : ' +'<b>'+ num_of_total_mirnas +'</b>' + '<p></p>');
  $('#modal1').append('- Unique microRNAs : ' +'<b>'+ (data.unique_mirnas_name_list).length +'</b>' + '&emsp;' );
  var sel = document.createElement('select');
  for (var i=0; i<(data.unique_mirnas_name_list).length; i++){
    var opt = document.createElement('OPTION');
    opt.setAttribute('value', data.unique_mirnas_name_list[i]);
    var t = document.createTextNode(data.unique_mirnas_name_list[i]);
    opt.appendChild(t);
    sel.appendChild(opt);
  }
  left_modal_body.appendChild(sel);
  $('#modal1').append('<p></p>');
  $('#modal1').append('- Minimum binding length : ' +'<b>'+ data.min_bind_len +'</b>' + '<p></p>');
  $('#modal1').append('- Maximum binding length : ' +'<b>'+ data.max_bind_len +'</b>' + '<p></p>');
  $('#modal1').append('- Average binding length : ' +'<b>'+ data.avg_bind_len +'</b>' + '<p></p>');
  $('#modal1').append('- 3\'UTR region binding rate : ' +'<b>'+ data.utr3_prob +'</b>' + '<p></p>');
  $('#modal1').append('- CDS region binding rate : ' +'<b>'+ data.cds_prob +'</b>' + '<p></p>');

  $('#modal1').append("- Conserved Species : "+'<b>'+ Object.keys(data.species_dict).length +'</b>' + '&emsp;' );
  sel = document.createElement('select');
  for(var index in data.species_dict) {
    opt = document.createElement('OPTION');
    opt.setAttribute('value', index);
    t = document.createTextNode(index);
    opt.appendChild(t);
    sel.appendChild(opt);
  }
  left_modal_body.appendChild(sel);
  $('#modal1').append('<p></p>');

  $('#modal1').append("- microRNA Families : "+'<b>' + Object.keys(data.families_contain).length +'</b>' + '&emsp;' );
  sel = document.createElement('select');
  for(var index in data.families_contain) {
    opt = document.createElement('OPTION');
    opt.setAttribute('value', index);
    t = document.createTextNode(index);
    opt.appendChild(t);
    sel.appendChild(opt);
  }
  left_modal_body.appendChild(sel);
  $('#modal1').append('<p></p>');

  //////////////////// Pie Charts /////////////////////////////
  var my_googleArray = [['Binding type' , 'interactions']];
  for(var index in data.bind_type_dict) {
    my_googleArray.push([index ,data.bind_type_dict[index] ])
  }
  //console.log('my_googleArray');
  //console.log(my_googleArray);

  //////------------------------------------------------///////
  var my_googleArray2 = [['Species' , 'Number of MREs conserved']];
  for(var index in data.species_dict) {
    if(index == 'NA'){
      continue;
    }
    my_googleArray2.push([index ,data.species_dict[index] ])
  }
  //console.log('my_googleArray2');
  //console.log(my_googleArray2);

   //////------------------------------------------------///////
  var my_googleArray3 = [['miR families' , 'interactions']];
  for(var index in data.families_contain) {
    my_googleArray3.push([index ,data.families_contain[index].length ])
  }
  //console.log('my_googleArray3');
  //console.log(my_googleArray3);
  ////// -------------------------------/////////////////

  // Load google charts
  google.charts.load('current', {'packages':['corechart']});
  google.charts.load("current", {packages: ["bar"]});
  google.charts.setOnLoadCallback(drawChart);
  google.charts.setOnLoadCallback(drawStuff);
  google.charts.setOnLoadCallback(drawChart3);

  // Draw the chart and set the chart values
  function drawChart() {
    //console.log(x);
    var data = google.visualization.arrayToDataTable(my_googleArray);
    var options = {chartArea:{left:5, top: 20, width: '90%', height: 360/(1920/windowWidth)},
                  'title':'Binding Types', width: '90%', 'height':360/(1920/windowWidth)
                };
    // Display the chart inside the <div> element with id="modal4"
    var chart = new google.visualization.PieChart(document.getElementById('modal4'));
    chart.draw(data, options);
  }

  // Draw the chart and set the chart values
  function drawStuff() {
    var data = google.visualization.arrayToDataTable(my_googleArray2);
    var options = {
          title: 'Conserved MREs per species',
          width: 500/(1920/windowWidth),
          height: 400,
          legend: { position: 'none' },
          chart: { title: 'Conserved MREs per species'},
          bars: 'horizontal',
          axes: {
            x: {
              0: { side: 'top', label: 'Number of MREs conserved'} // Top x-axis.
            }
          },
          bar: { groupWidth: "90%" }
        };
    // Display the chart inside the <div> element with id="modal2"
    var chart = new google.charts.Bar(document.getElementById('modal2'));
    chart.draw(data, options);
  }

  // Draw the chart and set the chart values
  function drawChart3() {
    var data = google.visualization.arrayToDataTable(my_googleArray3);
    var options = {chartArea:{left:5, top: 20, width: '90%', height: 360/(1920/windowWidth)},
                  'title':'MREs per Family', width: '90%', 'height':360/(1920/windowWidth)
                };
    // Display the chart inside the <div> element with id="modal3"
    var chart = new google.visualization.PieChart(document.getElementById('modal3'));
    chart.draw(data, options);
  }

  /***************** Modal Events *************************/
  $('#close-bt2 , #modal-close-bt').on('click', function(){
      modal.style.display = "none";
      $('#modal1').empty();
  });
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
          $('#modal1').empty();
      }
  }
}


/*--------------------------------------------------------------------------------------------*/
function resetSketch(){
  console.log('resetted');
  clear();
  console.log('Sketch reseted!');
}
/*--------------------------------------------------------------------------------------------*/
function draw(){
}
/*--------------------------------------------------------------------------------------------*/
