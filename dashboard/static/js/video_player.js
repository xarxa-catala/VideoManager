var video;
var configVideoPlayerId = 'video_player';
var configChaptersListId = 'video_player_chapters';
var configChapterClass = 'video_player_chapter';
var configCurrentChapterClass = 'current';
var configDataSource = 'vsource';
var configCurrentChapterTitleClass = 'video_player_current_chapter_title';

$(document).ready(function () {
  video = document.getElementById(configVideoPlayerId);
  let $vidosrc = $('#' + configChaptersListId + ' li:first-child .' + configChapterClass);
  $vidosrc.addClass(configCurrentChapterClass);
  $('.' + configCurrentChapterTitleClass).html($vidosrc.html());
  loadVideo($vidosrc.data(configDataSource));
});

$(document).on('click', '#' + configChaptersListId + ' .' + configChapterClass, function (e) {
  e.preventDefault();
  if (!$(this).hasClass(configCurrentChapterClass)) {
    $('#' + configChaptersListId + ' .' + configChapterClass + '.' +
      configCurrentChapterClass).removeClass(configCurrentChapterClass);
    $(this).addClass(configCurrentChapterClass);
    $('.' + configCurrentChapterTitleClass).html($(this).html());
    loadVideo($(this).data(configDataSource));
    video.play();
  }
});

function loadVideo(source)
{
  $('#' + configVideoPlayerId + ' #mp4').attr('src', source);
  video.load();
}
